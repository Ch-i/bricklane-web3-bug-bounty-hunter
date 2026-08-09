---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceRegulated::recordIssuance` to a platform wallet pollutes
  a shared `issuancesCounters[""]` bucket'
vuln_class: []
---

# `ComplianceServiceRegulated::recordIssuance` to a platform wallet pollutes a shared `issuancesCounters[""]` bucket

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceRegulated::recordIssuance` (lines 623-636) writes the issuance lock record under the recipient's investor id without gating on a non-empty id:

```solidity
function recordIssuance(address _to, uint256 _value, uint256 _issuanceTime) internal override returns (bool) {
    string memory investorTo = getRegistryService().getInvestor(_to);
    if (compareInvestorBalance(investorTo, _value, 0)) {
        adjustTotalInvestorsCounts(_to, CommonUtils.IncDec.Increase);
    }
    uint256 shares = getRebasingProvider().convertTokensToShares(_value);
    cleanupInvestorIssuances(investorTo);
    return createIssuanceInformation(investorTo, shares, _issuanceTime);
}
```

When `_to` is a platform wallet, `getInvestor(_to)` returns the empty string `""` (platform wallets have no entry in `investorsWallets`). `createIssuanceInformation("", shares, _issuanceTime)` at lines 737-749 then appends a record to `issuancesValues[""][issuancesCounters[""]]` and increments `issuancesCounters[""]`. The empty-string key acts as a shared global bucket across every issuance to any platform wallet across the protocol lifetime.

`ComplianceServiceRegulated::recordTransfer` (lines 600-621) calls `cleanupInvestorIssuances` for both legs:

```solidity
cleanupInvestorIssuances(investorFrom);
cleanupInvestorIssuances(investorTo);
```

Any transfer where either leg is a platform wallet calls `cleanupInvestorIssuances("")`. Inside `cleanupInvestorIssuances` (lines 890-932), `getCountry("")` returns `""` and `getCountryCompliance("")` returns `NONE` (0), so the else-branch sets `lockTime = getNonUSLockPeriod()`. The function then walks every record under `issuancesCounters[""]` swap-popping the ones with `issuanceTimestamp <= block.timestamp - lockTime`. Steady-state size of the bucket is roughly `(platform_wallet_issuance_frequency * nonUSLockPeriod)`.

**Files:**

`ComplianceServiceRegulated::recordIssuance`, `ComplianceServiceRegulated::createIssuanceInformation`, `ComplianceServiceRegulated::cleanupInvestorIssuances`

**Impact:** The gas cost on platform-wallet-leg transfers grows linearly with the steady-state bucket size, which is roughly `platform_wallet_issuance_rate * nonUSLockPeriod`. The bug fires only when MASTER or ISSUER mints directly to a platform wallet via `DSToken::issueTokens` and friends, which are gated on `onlyIssuerOrAbove` (MASTER + ISSUER only). Transfers to platform wallets do not pollute the bucket. The realistic deployment shape therefore determines the impact:

- Capital-event cadences typical of security tokens (~1-12 platform-wallet issuances per year): the bucket stays under ~20 records and the per-transfer cleanup overhead is negligible.
- Active or rebasing deployments with ~1 issuance per day over a 365-day lockup: the bucket reaches ~365 records and per-transfer overhead lands around 1M-3M gas - operationally painful (~30-60x normal cost) but transfers still fit in a block.
- Sustained high-frequency issuance (~10+/day): the bucket reaches several thousand records and per-transfer overhead approaches the block gas limit, bricking transfers.

Whether a deployment reaches a DoS threshold depends entirely on the issuer's own operational tempo. There is no external attacker class: only MASTER and ISSUER can mint, and only MASTER and ISSUER can designate platform wallets via `WalletManager::addPlatformWallet` (also `onlyIssuerOrAbove`). The bug is an issuer self-foot-gun whose blast radius is bounded by the issuer's own choices.

Recovery is available without an implementation upgrade: MASTER can prune the polluted bucket by walking `issuancesCounters[""]` / `issuancesValues[""]` / `issuancesTimestamps[""]` and clearing entries. The prune is O(N) in bucket size and may need to span multiple transactions for very large buckets, but it is a master-only operation that does not require coordinating an upgrade or a state rollback. Combined with the issuer-controlled trigger, no funds at risk (gas-cost-only impact), and the deployment-shape-dependent threshold, severity sits at Low.

The `getComplianceTransferableTokens` path is not affected because `checkHoldUp` is gated on `!_isPlatformWalletFrom` at line 141; the empty-key bucket never enters the transferability calculation. The damage is purely the gas cost on the transfer path.

**Proof of Concept:** Add the following test to `test/solace-pocs/L-1.test.ts` and run with: `npx hardhat test test/solace-pocs/L-1.test.ts`.

```typescript
// PoC: ComplianceServiceRegulated::recordIssuance to a platform wallet writes
// a lockup record under the empty-string investor id ("") because
// getRegistryService().getInvestor(platformWallet) returns "" (platform
// wallets are not registered investor wallets). createIssuanceInformation
// does not gate on a non-empty id, so the record lands in the shared
// issuancesValues[""][issuancesCounters[""]] slot. The bucket accumulates
// across every platform-wallet issuance and is never naturally pruned for
// records still within the lockup window.
//
// On every subsequent transfer touching a platform wallet (either leg),
// recordTransfer calls cleanupInvestorIssuances("") which scans the entire
// bucket. The per-transfer gas cost grows monotonically with the bucket
// size = platform_wallet_issuance_rate * nonUSLockPeriod.
//
// The mapping is internal, so this test observes the bug via the gas-cost
// side effect: a transfer to a platform wallet costs measurably more after
// the bucket has been polluted by repeated platform-wallet issuances. The
// gas overhead grows linearly with the issuance count.

import hre from 'hardhat';
import { expect } from 'chai';
import { loadFixture } from '@nomicfoundation/hardhat-toolbox/network-helpers';
import { deployDSTokenRegulated, INVESTORS } from '../utils/fixture';

describe('PoC: recordIssuance to a platform wallet pollutes issuancesCounters[""] and taxes every platform-wallet-leg transfer', function () {
  it('test_PoC_PlatformWalletBucketPollutionGrowsGasCost', async function () {
    const [
      deployer,
      regularInvestorWallet,
      platformWallet,
    ] = await hre.ethers.getSigners();

    const {
      dsToken,
      registryService,
      walletManager,
      complianceConfigurationService,
    } = await loadFixture(deployDSTokenRegulated);

    // Wide caps so the only gate exercised in this PoC is the issuancesCounters
    // bucket scan. USA mapped to US compliance so the regular investor has a
    // valid region.
    await complianceConfigurationService.setNonAccreditedInvestorsLimit(1000);
    await complianceConfigurationService.setTotalInvestorsLimit(1000);
    await complianceConfigurationService.setUSInvestorsLimit(1000);
    await complianceConfigurationService.setMinUSTokens(0);
    await complianceConfigurationService.setMinimumHoldingsPerInvestor(0);
    await complianceConfigurationService.setCountryCompliance(
      INVESTORS.Country.USA,
      INVESTORS.Compliance.US,
    );
    // Configure a non-zero non-US lockup period so records added to the empty-
    // string ("") bucket (the platform-wallet bucket, which evaluates under
    // countryCompliance == NONE -> else branch in cleanupInvestorIssuances) do
    // not instantly age out. With lockTime == 0, every cleanup call would
    // evict every record and the bucket would never grow - which is why the
    // bug is latent in default-config deployments and only bites when the
    // operator sets a real lockup period (the Reg-D Rule 144 12-month default
    // is typical).
    await complianceConfigurationService.setNonUSLockPeriod(365 * 24 * 60 * 60);
    await complianceConfigurationService.setUSLockPeriod(365 * 24 * 60 * 60);

    // Register the platform wallet via WalletManager (onlyIssuerOrAbove).
    // After this, isPlatformWallet(platformWallet) == true and
    // getRegistryService().getInvestor(platformWallet) == "" (platform
    // wallets have no entry in investorsWallets).
    await walletManager.addPlatformWallet(await platformWallet.getAddress());

    // Onboard a regular investor with a token balance for the test transfers.
    await registryService.registerInvestor(
      INVESTORS.INVESTOR_ID.US_INVESTOR_ID,
      INVESTORS.INVESTOR_ID.US_INVESTOR_COLLISION_HASH,
    );
    await registryService.setCountry(
      INVESTORS.INVESTOR_ID.US_INVESTOR_ID,
      INVESTORS.Country.USA,
    );
    await registryService.addWallet(
      await regularInvestorWallet.getAddress(),
      INVESTORS.INVESTOR_ID.US_INVESTOR_ID,
    );
    await dsToken.issueTokens(await regularInvestorWallet.getAddress(), 10000n);

    // Baseline: transfer 1 token from the regular investor to the platform
    // wallet while issuancesCounters[""] is still empty. recordTransfer's
    // cleanupInvestorIssuances("") call scans 0 records on the platform-wallet
    // leg. Record gas used.
    const baselineTx = await dsToken
      .connect(regularInvestorWallet)
      .transfer(await platformWallet.getAddress(), 1n);
    const baselineReceipt = await baselineTx.wait();
    const baselineGas = baselineReceipt!.gasUsed;

    // Pollute the bucket: issue tokens directly to the platform wallet 50
    // times. Each call writes a new record under
    // issuancesValues[""][issuancesCounters[""]] and increments
    // issuancesCounters[""]. After this loop the bucket holds 50 phantom
    // records that will not naturally expire until nonUSLockPeriod elapses.
    const POLLUTION_COUNT = 50n;
    for (let i = 0n; i < POLLUTION_COUNT; i++) {
      await dsToken.issueTokens(await platformWallet.getAddress(), 1n);
    }

    // After-pollution: same transfer shape. cleanupInvestorIssuances("") now
    // scans the polluted 50-record bucket on every platform-wallet-leg
    // transfer.
    const afterTx = await dsToken
      .connect(regularInvestorWallet)
      .transfer(await platformWallet.getAddress(), 1n);
    const afterReceipt = await afterTx.wait();
    const afterGas = afterReceipt!.gasUsed;

    // BUG ASSERTION: the post-pollution transfer costs strictly more than the
    // baseline, with the overhead attributable to the bucket scan. The exact
    // gas delta depends on chain config (cold vs warm SLOADs, EIP-2929
    // gas schedule), but at this bucket size the scan adds at least ~50K gas.
    // For larger steady-state buckets the overhead grows linearly toward the
    // block gas limit; this finding's body walks the deployment-shape spectrum.
    expect(afterGas).to.be.gt(baselineGas);
    expect(afterGas - baselineGas).to.be.gt(50000n);

    // Sanity: the transfers actually executed, no partial revert hidden behind
    // the assertion.
    expect(await dsToken.balanceOf(await platformWallet.getAddress())).to.equal(
      52n, // 1 (baseline) + 50 (pollution) + 1 (after-pollution)
    );
  });
});
```

Test result on the unfixed codebase:

```
PoC: recordIssuance to a platform wallet pollutes issuancesCounters[""] and taxes every platform-wallet-leg transfer
  ✔ test_PoC_PlatformWalletBucketPollutionGrowsGasCost (1293ms)

1 passing (1s)
```

The test reproduces the bucket pollution end-to-end under normal Issuer operations. The baseline platform-wallet-leg transfer runs `cleanupInvestorIssuances("")` against an empty bucket. After 50 platform-wallet issuances, the same transfer shape runs the cleanup against a 50-record bucket and pays >50K more gas. The overhead grows linearly with the bucket size, so the per-transfer cost compounds as the issuer continues to fund platform wallets via direct issuance. The default `nonUSLockPeriod = 0` config masks the bug (records age out instantly), which is why the test explicitly sets a 365-day lockup mirroring the Reg-D Rule 144 default.

**Recommended Mitigation:** Gate `createIssuanceInformation` on `!CommonUtils.isEmptyString(investorTo)` inside `recordIssuance`, mirroring the gate at `TokenLibrary::updateInvestorBalance` that already prevents the empty-string key from being written for the `investorsBalances` mapping:

```solidity
function recordIssuance(address _to, uint256 _value, uint256 _issuanceTime) internal override returns (bool) {
    string memory investorTo = getRegistryService().getInvestor(_to);
    if (compareInvestorBalance(investorTo, _value, 0)) {
        adjustTotalInvestorsCounts(_to, CommonUtils.IncDec.Increase);
    }
    if (CommonUtils.isEmptyString(investorTo)) {
        return true;
    }
    uint256 shares = getRebasingProvider().convertTokensToShares(_value);
    cleanupInvestorIssuances(investorTo);
    return createIssuanceInformation(investorTo, shares, _issuanceTime);
}
```

Platform-wallet issuances do not need per-investor lockup tracking because platform wallets are exempt from the lockup check (the `checkHoldUp` short-circuit at line 141). Skipping the record write at issuance time is invariant-preserving and eliminates the bucket pollution at its source.

To remediate already-polluted state on already-deployed instances, the `onlyMaster` recovery override would have to walk and clear `issuancesCounters[""]` / `issuancesValues[""]` / `issuancesTimestamps[""]`; in practice an off-chain mass-prune transaction submitted by the master role after the fix lands is the only way to drain the bucket.

**Securitize:** Fixed in [31d2289](https://github.com/securitize-io/dstoken/commit/31d2289057e1cca2a4246ebb8c648bd4d094694a).

**Cyfrin:** Verified.
