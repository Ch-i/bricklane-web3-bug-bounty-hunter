---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceRegulated::adjustInvestorsCountsByCountry` double-increment
  bricks non-accredited onboarding'
vuln_class: []
---

# `ComplianceServiceRegulated::adjustInvestorsCountsByCountry` double-increment bricks non-accredited onboarding

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** The finding is a composite of two latent defects that together produce protocol-wide denial of service on non-accredited investor onboarding.

The first is a producer-side double-increment in `ComplianceServiceRegulated::adjustInvestorsCountsByCountry` (`contracts/compliance/ComplianceServiceRegulated.sol:688-735`). The function unconditionally increments `accreditedInvestorsCount` whenever `isAccreditedInvestor(_id)` is true, regardless of whether the country resolves to a known compliance region. The regional branches (US, EU, JP) are gated on `countryCompliance`; the accredited branch is not. When an investor is registered, accredited, and receives tokens BEFORE `setCountry` is called - a sequence the protocol does not prohibit - `recordIssuance` invokes the function with `country == ""`. The empty-country path skips the regional branches but increments `accreditedInvestorsCount`. The subsequent `setCountry` calls `adjustInvestorCountsAfterCountryChange` with `prevCountry = ""`, which skips the Decrease branch (gated on `bytes(_prevCountry).length > 0`) but unconditionally invokes `adjustInvestorsCountsByCountry` again with the new country, incrementing `accreditedInvestorsCount` a second time. `totalInvestors` is incremented only once (only `adjustTotalInvestorsCounts` touches it). End state per investor that traverses this lifecycle order: `accreditedInvestorsCount` is incremented by 2 while `totalInvestors` is incremented by 1; the invariant `accreditedInvestorsCount <= totalInvestors` drifts by 1.

The second is a consumer-side checked-arithmetic underflow. Two consumer sites compute the non-accredited investor headroom as `getTotalInvestorsCount() - getAccreditedInvestorsCount()` directly under Solidity 0.8 checked arithmetic: `ComplianceServiceLibrary::maxInvestorsInCategoryForNonAccredited` (`contracts/compliance/ComplianceServiceRegulated.sol:156-172`) used inside `completeTransferCheck`, and `ComplianceServiceRegulated::preIssuanceCheck` (`contracts/compliance/ComplianceServiceRegulated.sol:484`) used at issuance time. Both should saturate at zero when the cap is breached; instead they revert with `Panic(0x11)` (arithmetic underflow) when the operands invert. Once the producer-side double-increment has driven `accreditedInvestorsCount > totalInvestorsCount` by any amount, every onward call to either consumer site reverts with an opaque arithmetic panic.

The bug is reachable via two paths. The first is a single-tenant lifecycle ordering bug: any honest EXCHANGE that uses the documented-valid order `registerInvestor -> setAttribute -> addWallet -> issueTokens -> setCountry` on one of their own accredited investors fires the double-increment by accident, with no cross-tenant interaction. The second is a cross-tenant attribute hijack: an attacker EXCHANGE re-attributes a victim investor (created by a different EXCHANGE) from non-accredited to accredited via `setAttribute`, then the next issuance traverses the asymmetric branch with the same effect. Both paths produce the same on-chain corruption shape; the lifecycle-ordering path is sufficient to reach the DoS without an attacker.

**Files:**

`ComplianceServiceRegulated::adjustInvestorsCountsByCountry`, `ComplianceServiceRegulated::adjustInvestorCountsAfterCountryChange`, `ComplianceServiceLibrary::maxInvestorsInCategoryForNonAccredited`, `ComplianceServiceRegulated::preIssuanceCheck`

**Impact:** The defect surface has two distinguishable sub-components:

**M-3.a - Producer-side double-increment.** Each accredited investor that traverses the empty-country issuance -> `setCountry` lifecycle drifts `accreditedInvestorsCount` ahead of `totalInvestors` by 1. The drift is silent: no error fires at the time of corruption, no event marks the imbalance, and the counters are only inspected by the consumer sites at the next cap-check. Drift accumulates across investors and across normal protocol operations until a non-accredited investor onboarding tries to fire the consumer subtraction.

**M-3.b - Consumer-side denial of service.** Once `accreditedInvestorsCount > totalInvestors` by even one, every non-accredited issuance and every non-accredited new-investor transfer reverts with `Panic(0x11)`. No error string, no compliance code, no pointer to which counter is corrupt. From an operator's perspective, the failure mode is opaque and protocol-wide: every non-accredited onboarding stops working at once, with the trace pointing only to an arithmetic underflow inside the regulated compliance library. The cap-check sits on the critical path for the most common onboarding flow (non-accredited retail investors hitting the regional caps), so the practical effect is total cessation of non-accredited onboarding for the affected token.

The attacker class is the EXCHANGE role - a trusted multi-tenant integration partner under the protocol's documented trust model - but Path A (the single-tenant lifecycle ordering bug) is reachable without any cross-tenant interaction; an honest exchange following a valid onboarding sequence is enough to fire the bug. No user funds are at risk: the bug is denial of service on the onboarding path, no tokens are lost or moved, and balances on already-onboarded investors are unaffected.

The on-chain corruption is recoverable by MASTER without an implementation upgrade. `ComplianceServiceRegulated` exposes `setAccreditedInvestorsCount(uint256)` and the five sibling counter setters as `onlyMaster` functions at `contracts/compliance/ComplianceServiceRegulated.sol:854-888`, each a plain assignment to the corresponding storage slot. After detecting the inverted invariant (visible via `getAccreditedInvestorsCount` and `getTotalInvestorsCount` reads, and signposted by the `Panic(0x11)` revert on every non-accredited onboarding), MASTER computes the correct `accreditedInvestorsCount` off-chain by replaying the issuance/transfer/burn/seize/setCountry history under the intended counter logic, and writes the corrected value via `setAccreditedInvestorsCount`. The DoS lifts immediately for new onboarding. The recovery is a fiat overwrite rather than a state rollback, and it has to be re-applied after every retrigger (an honest accredited-investor onboarding under the wrong lifecycle order is enough to re-corrupt the counter), but the recovery is simple, on-chain, and does not require coordinating an implementation upgrade.

**Proof of Concept:** Add the following test to `test/solace-pocs/M-3.test.ts` and run with: `npx hardhat test test/solace-pocs/M-3.test.ts`.

```typescript
// PoC: Bricks non-accredited onboarding by driving accreditedInvestorsCount
// above totalInvestorsCount. The bug is reachable via a single-tenant
// lifecycle ordering (no cross-tenant interaction required) - any honest
// EXCHANGE using the documented-valid order
// registerInvestor -> setAttribute(ACCREDITED) -> addWallet -> issueTokens
// -> setCountry on an accredited investor fires the double-increment.
//
// Producer-side mechanism (ComplianceServiceRegulated::adjustInvestorsCountsByCountry,
// lines 688-735): the accredited branch is gated only on isAccreditedInvestor,
// not on countryCompliance. So with country "" (default after registerInvestor
// before setCountry), the first issuance increments accreditedInvestorsCount
// while totalInvestors increments by 1 (total path). Then setCountry triggers
// adjustInvestorCountsAfterCountryChange("US", ""), which skips the Decrease
// branch (prev country is "") and unconditionally invokes
// adjustInvestorsCountsByCountry with the new country - incrementing
// accreditedInvestorsCount a SECOND time. totalInvestors is NOT touched.
// End state: accreditedInvestorsCount = 2, totalInvestors = 1.
//
// Consumer-side mechanism (preIssuanceCheck:484 and
// maxInvestorsInCategoryForNonAccredited:156-172): both compute
// totalInvestorsCount - accreditedInvestorsCount under Solidity 0.8 checked
// arithmetic. Once the producer-side drift inverts the operands, every
// non-accredited onboarding reverts with Panic(0x11).

import hre from 'hardhat';
import { expect } from 'chai';
import { loadFixture, time } from '@nomicfoundation/hardhat-toolbox/network-helpers';
import { deployDSTokenRegulated, INVESTORS } from '../utils/fixture';
import { DSConstants } from '../../utils/globals';

describe('PoC: accreditedInvestorsCount > totalInvestorsCount bricks non-accredited onboarding', function () {
  it('test_PoC_NonAccreditedOnboardingDoSViaLifecycleOrdering', async function () {
    const [deployer, accreditedWallet, nonAccreditedWallet] = await hre.ethers.getSigners();

    const {
      dsToken,
      registryService,
      complianceService,
      complianceConfigurationService,
    } = await loadFixture(deployDSTokenRegulated);

    // Configure the non-accredited cap so the consumer subtraction is reached
    // by every non-accredited onboarding. Pick a value large enough that the
    // cap itself is not the gating concern - we want to demonstrate the
    // underflow, not the cap-rejection.
    await complianceConfigurationService.setNonAccreditedInvestorsLimit(100);
    await complianceConfigurationService.setCountryCompliance(
      INVESTORS.Country.USA,
      INVESTORS.Compliance.US,
    );

    // Lifecycle Path A: registerInvestor -> setAttribute(ACCREDITED) -> addWallet
    // -> issueTokens -> setCountry. All steps are valid honest-EXCHANGE operations.
    const accreditedId = INVESTORS.INVESTOR_ID.US_INVESTOR_ID;

    // Step A1: register the investor with empty country (default).
    await registryService.registerInvestor(accreditedId, '');

    // Step A2: mark the investor as ACCREDITED. setAttribute fires no compliance
    // hook, so counters are unchanged at this point.
    const futureExpiry = (await time.latest()) + 365 * 24 * 60 * 60;
    await registryService.setAttribute(
      accreditedId,
      DSConstants.attributeType.ACCREDITED,
      DSConstants.attributeStatus.APPROVED,
      futureExpiry,
      'ipfs://accreditation-proof-cid',
    );

    // Step A3: attach the wallet.
    await registryService.addWallet(await accreditedWallet.getAddress(), accreditedId);

    // Step A4: issue tokens to the accredited investor BEFORE setCountry.
    // This is the operation that fires the first accredited++ via the empty-country
    // path through adjustInvestorsCountsByCountry.
    await dsToken.issueTokens(await accreditedWallet.getAddress(), 100n);

    // After issuance the counters are still consistent: the empty-country path
    // skips the regional branches but increments the unconditional accredited
    // branch once. totalInvestors goes from 0 -> 1 alongside.
    expect(await complianceService.getTotalInvestorsCount()).to.equal(1n);
    expect(await complianceService.getAccreditedInvestorsCount()).to.equal(1n);

    // Step A5: set the country to "USA". This is the trigger: the
    // setCountry path -> adjustInvestorCountsAfterCountryChange skips the
    // Decrease branch (prev country was "") and unconditionally invokes
    // adjustInvestorsCountsByCountry with the new country, firing the
    // accredited branch a SECOND time. totalInvestors is NOT touched.
    await registryService.setCountry(accreditedId, INVESTORS.Country.USA);

    // BUG ASSERTION: the invariant accreditedInvestorsCount <= totalInvestors
    // is now violated.
    expect(await complianceService.getTotalInvestorsCount()).to.equal(1n);
    expect(await complianceService.getAccreditedInvestorsCount()).to.equal(2n);

    // Consumer-side trigger: try to onboard a non-accredited investor. The
    // preIssuanceCheck path reaches totalInvestorsCount - accreditedInvestorsCount
    // = 1 - 2 and reverts with Panic(0x11) (Solidity 0.8 checked-arithmetic
    // underflow). Ethers surfaces this as a Panic with code 0x11.
    const nonAccreditedId = INVESTORS.INVESTOR_ID.US_INVESTOR_ID_2;
    await registryService.registerInvestor(nonAccreditedId, INVESTORS.Country.USA);
    await registryService.addWallet(await nonAccreditedWallet.getAddress(), nonAccreditedId);

    // No accreditation attribute set -> isAccreditedInvestor(nonAccreditedId) == false
    // -> the cap subtraction at preIssuanceCheck:484 fires on this issuance.
    await expect(
      dsToken.issueTokens(await nonAccreditedWallet.getAddress(), 100n),
    ).to.be.revertedWithPanic(0x11);

    // Confirm the destination wallet's balance is unchanged - the issuance
    // truly reverted, no partial state mutation.
    expect(await dsToken.balanceOf(await nonAccreditedWallet.getAddress())).to.equal(0n);

    // Recovery primitive: MASTER can lift the DoS by overwriting the corrupted
    // counter via the onlyMaster setter at ComplianceServiceRegulated.sol:872.
    // (Demonstrate, but do not rely on - this is the in-scope recovery path
    //  the finding's Medium-severity rationale references.)
    await complianceService.setAccreditedInvestorsCount(1);
    expect(await complianceService.getAccreditedInvestorsCount()).to.equal(1n);

    // After the MASTER recovery write, non-accredited onboarding works again.
    await expect(
      dsToken.issueTokens(await nonAccreditedWallet.getAddress(), 100n),
    ).to.not.be.reverted;
    expect(await dsToken.balanceOf(await nonAccreditedWallet.getAddress())).to.equal(100n);
  });
});
```

Test result on the unfixed codebase:

```
PoC: accreditedInvestorsCount > totalInvestorsCount bricks non-accredited onboarding
  test_PoC_NonAccreditedOnboardingDoSViaLifecycleOrdering (1206ms)
1 passing (1s)
```

The test reproduces the bug end-to-end via Path A (single-tenant lifecycle ordering, no cross-tenant interaction required). The producer-side double-increment fires when the accredited investor traverses the empty-country issuance leg, leaving `accreditedInvestorsCount = 2` and `totalInvestors = 1` after `setCountry`. The next non-accredited onboarding attempt reverts with `Panic(0x11)` at the consumer subtraction. The test also demonstrates the recovery primitive: `setAccreditedInvestorsCount(1)` (MASTER-only) lifts the DoS without an implementation upgrade. Applying either the producer-side fix (gate the accredited branch on `countryCompliance != 0`) or the consumer-side fix (saturating-at-zero subtraction in `maxInvestorsInCategoryForNonAccredited` and `preIssuanceCheck`) breaks the chain at the source.

**Recommended Mitigation:** Two independent fixes; either alone breaks the chain, together they are defense-in-depth.

1. **Producer-side fix (closes M-3.a at the source).** Either gate the accredited branch in `adjustInvestorsCountsByCountry` on `countryCompliance != 0`, mirroring the regional branches, so the empty-country path does not increment `accreditedInvestorsCount` (the subsequent `setCountry` will then increment it correctly exactly once); or force the lifecycle order by rejecting issuance to investors whose country is the empty string inside `validateIssuance`/`recordIssuance`. The first preserves the current onboarding ordering flexibility; the second forces `setCountry` to happen before any issuance.

2. **Consumer-side fix (closes M-3.b structurally, regardless of producer state).** Replace the bare subtraction at the two consumer sites with a saturating-at-zero form:

   ```solidity
   uint256 nonAccredited = totalInvestors > accreditedInvestorsCount
       ? totalInvestors - accreditedInvestorsCount
       : 0;
   ```

 OpenZeppelin's `Math::zeroFloorSub` provides this primitive. The cap check then rejects only when the cap is genuinely breached, instead of reverting on the subtraction itself. This closes the DoS regardless of how the producer-side counter drift is reached, including via cross-tenant attribute hijack or any future refactor that re-introduces a similar imbalance.

3. **Cross-counter invariant guards on the recovery primitive.** Add bounds-check requires on `setAccreditedInvestorsCount`, `setTotalInvestorsCount`, `setUSInvestorsCount`, and `setUSAccreditedInvestorsCount` so MASTER cannot inadvertently re-create the underflow via a mistyped recovery value. Each setter should enforce the cross-counter constraint inline (`require(_value <= totalInvestorsCount)` on `setAccreditedInvestorsCount`, the symmetric guard on `setTotalInvestorsCount`, etc.) so a corrective write cannot leave the consumer in a panic state.

**Securitize:** Fixed in [f078925](https://github.com/securitize-io/dstoken/commit/f0789253ce4ef5a995dba91f5c235e6f3e64181f).

**Cyfrin:** Verified.
