---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-0-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: Platform-wallet routing bypasses the active non-US-to-US flowback restriction
vuln_class: []
---

# Platform-wallet routing bypasses the active non-US-to-US flowback restriction

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceRegulated` enforces a regulatory flowback window via `blockFlowbackEndTime`. While that timestamp is in the future, a non-US investor must not be able to move tokens to a US investor: the resulting transfer is intended to revert with the `Flowback` reason. The check, however, is implemented only on the direct non-US-sender → US-recipient leg, and is unconditionally skipped on both legs that involve a platform wallet. A non-US investor can therefore reach a US investor by routing through any address that the operator has registered as a platform wallet, even though the direct transfer between the same two parties would be rejected.

There are two distinct gaps in `contracts/compliance/ComplianceServiceRegulated.sol` that combine to produce the bypass.

**Gap 1 — `doPreTransferCheckRegulated` returns `VALID` from the platform-recipient branch before any country-pair check runs.**

For any transfer whose recipient is a platform wallet, the pre-transfer check evaluates a single guard (force-full-transfer) and then short-circuits with `(0, VALID)`. None of the country / region rules in `completeTransferCheck` — including the flowback branch — are ever reached on this leg.

```solidity
// contracts/compliance/ComplianceServiceRegulated.sol
uint256 fromInvestorBalance = balanceOfInvestor(_services, _from);
uint256 fromRegion = getCountryCompliance(_services, _from);
bool isPlatformWalletTo = IDSWalletManager(_services[WALLET_MANAGER]).isPlatformWallet(_to);
if (isPlatformWalletTo) {
    if (
        ((IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getForceFullTransfer()
        && (fromRegion == US)) ||
        IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getWorldWideForceFullTransfer()) &&
        fromInvestorBalance > _value
    ) {
        return (50, ONLY_FULL_TRANSFER);
    }
    return (0, VALID); // <-- skips completeTransferCheck, including the flowback branch
}

// ...
CompletePreTransferCheckArgs memory args = CompletePreTransferCheckArgs(
    _from, _to, _value, fromInvestorBalance, fromRegion, isPlatformWalletTo
);
return completeTransferCheck(_services, args);
```

Because the early return fires before `completeTransferCheck`, a non-US investor sending to a platform wallet is never measured against the flowback window, regardless of how the platform wallet is going to redistribute the tokens afterwards.

**Gap 2 — `completeTransferCheck` exempts platform-wallet senders from the flowback branch.**

On the outbound leg the function does reach the non-US sender branch, but the flowback condition explicitly requires `!isPlatformWalletFrom`. As soon as the sender is registered as a platform wallet, the branch is disabled and the transfer falls through to the rest of the function:

```solidity
// contracts/compliance/ComplianceServiceRegulated.sol
bool isPlatformWalletFrom = IDSWalletManager(_services[WALLET_MANAGER]).isPlatformWallet(_args.from);

if (_args.fromRegion == US) {
    // ... US-sender rules
} else {
    if (checkHoldUp(_services, _args.from, _args.value, false, isPlatformWalletFrom)) {
        return (33, HOLD_UP);
    }

    if (
        toRegion == US &&
        !isPlatformWalletFrom && // <-- disables flowback whenever the sender is a platform wallet
        isBlockFlowbackEndTimeOk(
            IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getBlockFlowbackEndTime()
        )
    ) {
        return (25, FLOWBACK);
    }
    // ... falls through and the transfer to the US investor is accepted
}
```

Note also that the branch keys on `_args.fromRegion`, i.e. the *current sender's* configured country region. A platform wallet typically has no country set (region is `NONE`), so even without the explicit `!isPlatformWalletFrom` guard the outbound leg would not enter the non-US-sender branch. The flowback rule is intrinsically tied to the *original* sender's region, which is lost the moment tokens move into platform custody.

**End-to-end consequence.** The composition of the two gaps produces the bypass:

1. `nonUS_investor → US_investor`: `completeTransferCheck` runs with `fromRegion == EU/NONE-US` and `toRegion == US`, the flowback branch matches, the call reverts with `Flowback`.
2. `nonUS_investor → platform_wallet`: `doPreTransferCheckRegulated` returns `(0, VALID)` from the platform-recipient early return; flowback is never evaluated.
3. `platform_wallet → US_investor`: `completeTransferCheck` runs, but the platform-sender exemption (and the lost original region) disables the flowback branch; the transfer succeeds.

The end state is that the non-US holder's tokens land in a US investor's balance while `blockFlowbackEndTime` is still in the future, which is exactly the state the rule is meant to prevent. This is distinct from the platform-wallet lock-up, pause, and investor-cap bypasses reported separately — the control circumvented here is specifically the active flowback window.

**Impact:** The configured flowback window is not a reliable non-US-to-US transfer restriction. Tokens that cannot move directly from a non-US investor to a US investor can reach the US investor through platform custody while `blockFlowbackEndTime` is still active, which defeats the regulatory purpose of the timer (preventing premature flowback of off-shore-distributed tokens into the US market).

**Proof of Concept:** The following Hardhat test is self-contained: it configures France as EU, USA as US, sets a future `blockFlowbackEndTime`, registers a French holder and a US recipient, confirms that the direct transfer reverts with `Flowback`, and then demonstrates that the same tokens can reach the US investor by routing through a platform wallet.

```typescript
// test/audit-platform-flowback-bypass-poc.test.ts
import { expect } from 'chai';
import hre from 'hardhat';
import { loadFixture, time } from '@nomicfoundation/hardhat-network-helpers';

// Minimal inline equivalents of the project's test helpers so this PoC is
// readable on its own. The real fixtures live under test/utils/.
const DAYS = 24 * 60 * 60;

const Compliance = { EU: 2, US: 4 }; // values from contracts/utils/CommonUtils.sol
const FRANCE = 'france';
const USA = 'usa';
const FRENCH_INVESTOR_ID = 'frenchInvestorId';
const US_INVESTOR_ID = 'usInvestorId';

async function deployDSTokenRegulated() {
  // Re-uses the project's deploy-all Hardhat task which wires up DSToken,
  // ComplianceServiceRegulated, RegistryService, WalletManager, and the
  // ComplianceConfigurationService that the test interacts with below.
  return hre.run('deploy-all', { name: 'Token Example 1', symbol: 'TX1', decimals: 2 });
}

async function registerInvestor(investorId: string, wallet: any, registryService: any) {
  await registryService.registerInvestor(investorId, '');
  await registryService.addWallet(wallet, investorId);
}

describe('Audit PoC: platform wallet flowback bypass', function () {
  it('routes non-US tokens to a US investor through a platform wallet while flowback is active', async function () {
    const [nonUSHolder, usRecipient, platform] = await hre.ethers.getSigners();
    const {
      dsToken,
      registryService,
      complianceConfigurationService,
      walletManager,
    } = await loadFixture(deployDSTokenRegulated);

    // 1. Configure the regulatory state.
    await complianceConfigurationService.setCountryCompliance(FRANCE, Compliance.EU);
    await complianceConfigurationService.setCountryCompliance(USA, Compliance.US);
    await complianceConfigurationService.setEURetailInvestorsLimit(100);
    // Flowback window is open for ~1 day from now.
    await complianceConfigurationService.setBlockFlowbackEndTime((await time.latest()) + DAYS);

    // 2. Onboard a French (EU) holder and a US recipient.
    await registerInvestor(FRENCH_INVESTOR_ID, nonUSHolder, registryService);
    await registerInvestor(US_INVESTOR_ID, usRecipient, registryService);
    await registryService.setCountry(FRENCH_INVESTOR_ID, FRANCE);
    await registryService.setCountry(US_INVESTOR_ID, USA);

    // 3. Issue tokens to the French holder.
    await dsToken.issueTokens(nonUSHolder, 100);

    // 4. The direct French -> US transfer is correctly blocked by the flowback rule.
    await expect(dsToken.connect(nonUSHolder).transfer(usRecipient, 10))
      .to.be.revertedWith('Flowback');

    // 5. Operator registers a platform wallet (no country, no investor record).
    await walletManager.addPlatformWallet(platform);

    // 6. Leg 1: French holder -> platform wallet. Succeeds because
    //    doPreTransferCheckRegulated returns VALID from the platform-recipient
    //    early return, skipping completeTransferCheck and therefore the
    //    flowback branch.
    await expect(dsToken.connect(nonUSHolder).transfer(platform, 100)).not.to.be.reverted;

    // 7. Leg 2: Platform wallet -> US investor. Succeeds because the flowback
    //    branch in completeTransferCheck is gated by `!isPlatformWalletFrom`,
    //    and the sender's region is no longer EU once tokens sit in the
    //    platform wallet.
    await expect(dsToken.connect(platform).transfer(usRecipient, 10)).not.to.be.reverted;

    // 8. US investor now holds the tokens despite the flowback window being
    //    open — the exact state the rule is meant to prevent.
    expect(await dsToken.balanceOf(usRecipient)).to.equal(10);
  });
});
```

Run with:

```bash
npx hardhat test test/audit-platform-flowback-bypass-poc.test.ts
```

Expected output: the test passes, which corresponds to the US recipient receiving 10 tokens from a non-US source while `blockFlowbackEndTime` is still in the future.

**Recommended Mitigation:** Evaluate the flowback restriction before any platform-wallet shortcut, and do not give platform-wallet senders an implicit exemption. Two changes are required:

1. **Inbound leg** — in `doPreTransferCheckRegulated`, move (or duplicate) the flowback check so that it runs *before* the platform-recipient early return. A transfer from a non-US holder into a platform wallet during the flowback window should be rejected unless an explicit exception applies.

2. **Outbound leg** — in `completeTransferCheck`, drop the `!isPlatformWalletFrom` exemption from the flowback branch, and key the rule on the *original* non-US origin rather than on the current sender's region (e.g. by tracking the source region for tokens held in platform custody, or by treating platform-wallet outflows to US investors as flowback-restricted by default).

A minimal first step that closes the direct bypass is:

```solidity
// Before any platform-recipient early return
if (
    toRegion == US &&
    fromRegion != US &&
    isBlockFlowbackEndTimeOk(
        IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getBlockFlowbackEndTime()
    )
) {
    return (25, FLOWBACK);
}
```

and removing `!isPlatformWalletFrom` from the existing flowback branch in `completeTransferCheck`.

If there is an operational reason for platform wallets to distribute to US investors during the flowback window (for example, primary distribution of US-tranche tokens that were temporarily held in custody), that exception should be expressed as an explicit, separately-configured rule (e.g. a per-wallet or per-tranche flag), documented as overriding the non-US-to-US flowback control, and not provided implicitly via the "sender is a platform wallet" predicate.


**Securitize:** Acknowledged; This is a genuine bypass but the fix has real operational trade-offs. Removing !isPlatformWalletFrom closes the bypass with a single-line change, but it may surprise operators who fund US investors from treasury platform wallets during a flowback window. This deserves a product-level decision before applying the fix. For now we are acknowledging this one.
