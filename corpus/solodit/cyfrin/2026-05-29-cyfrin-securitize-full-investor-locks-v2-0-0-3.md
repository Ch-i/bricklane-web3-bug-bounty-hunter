---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-0-3
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
title: '`ComplianceServiceLibrary::completeTransferCheck` EU retail cap skip clause
  over-extends to qualified senders'
vuln_class: []
---

# `ComplianceServiceLibrary::completeTransferCheck` EU retail cap skip clause over-extends to qualified senders

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** The EU retail cap in `ComplianceServiceLibrary::completeTransferCheck` is structured at `contracts/compliance/ComplianceServiceRegulated.sol:340-350` as:

```solidity
} else if (toRegion == EU) {
    if (
        isRetail(_services, _args.to) &&
        ComplianceServiceRegulated(...).getEURetailInvestorsCount(toCountry) >= ...getEURetailInvestorsLimit() &&
        isNewInvestor(toInvestorBalance) &&
        (!CommonUtils.isEqualString(getCountry(_services, _args.from), toCountry) ||
        (_args.fromInvestorBalance > _args.value && isRetail(_services, _args.from)))
    ) {
        return (40, MAX_INVESTORS_IN_CATEGORY);
    }
    ...
```

The fourth conjunct (the cap-skip clause) at line 347 reads `(_args.fromInvestorBalance > _args.value && isRetail(_args.from))`. It is meant to exempt transfers in which the sender's retail decrement on `adjustInvestorsCountsByCountry` offsets the recipient's retail increment, leaving `euRetailInvestorsCount[country]` unchanged. The increment-side logic at `contracts/compliance/ComplianceServiceRegulated.sol:720-726` decrements `euRetailInvestorsCount[_country]` only when `countryCompliance == EU && !isQualifiedInvestor(_id)`, so the genuine offset case is `same country AND sender is retail AND sender depletes balance` (a successful transfer requires `fromBal >= value`, so "depletes" means `fromBal == value`).

The bug is that the two sender-side predicates are coupled with AND. The inner AND `(fromBal > value && isRetail(from))` evaluates true only for retail retainers; for every other combination it collapses to false and the cap-skip carve-out applies. In the same-country branch the 4th conjunct simplifies to just the inner AND, so:

- Retail depleter (`fromBal == value`, `isRetail == true`): inner AND = `false && true = false`. 4th conjunct false, cap permissive. Real offset (`-1` retail from sender depleting matches `+1` retail from recipient). Correct, carve-out works.
- Retail retainer (`fromBal > value`, `isRetail == true`): inner AND = `true && true = true`. 4th conjunct true, cap fires. Sender retains balance so no decrement, no offset. Correct.
- Qualified depleter (`fromBal == value`, `isRetail == false`): inner AND = `false && false = false`. 4th conjunct false, cap permissive. Qualified senders never touch `euRetailInvestorsCount`, so no offset. Bug, cap should fire but skips.
- Qualified retainer (`fromBal > value`, `isRetail == false`): inner AND = `true && false = false`. 4th conjunct false, cap permissive. No offset. Bug, cap should fire but skips.

Cross-country (`!isEqualString(fromCountry, toCountry) == true`): 4th conjunct true via the outer OR, cap fires unconditionally. Correct, the recipient's `+1` lands on `euRetailInvestorsCount[toCountry]` and the sender's decrement (if any) lands on a different country's counter, so there is no offset.

The carve-out is therefore correctly applied to retail depleters (the intended offset case) but incorrectly extends to qualified senders (any balance) because the AND short-circuits to false whenever `isRetail(from)` is false. The carve-out should narrowly apply to retail depleters only.

The structurally analogous US-accredited cap at `contracts/compliance/ComplianceServiceRegulated.sol:381` is written with three OR-joined disjuncts and no nested AND: `(_args.fromRegion != US || !isAccredited(_services, _args.from) || _args.fromInvestorBalance > _args.value)`. Inverted, the cap fires unless `same region AND sender is accredited AND sender depletes balance`, exactly the offset shape, with no over-extension to non-accredited senders. The EU retail cap should mirror this three-OR layout.

**Impact:** Walking the qualified-sender bypass on a concrete deployment:

- State pre-transaction: `euRetailInvestorsLimit = 50`, `euRetailInvestorsCount["DE"] = 50` (cap reached). Investor `I_q` in country `DE` with `isQualifiedInvestor("I_q") = true`, balance 200. Investor `I_r` in country `DE` retail, balance 0, whitelisted.
- `I_q`'s wallet calls `DSToken::transfer(W_r, 100)`.
- At the EU retail cap check (lines 340-348) the 4th conjunct evaluates `(!isEqualString("DE","DE") || (200 > 100 && isRetail(I_q)))` = `(false || (true && false))` = `false`. The cap-rejection branch is therefore NOT taken. The transfer proceeds.
- `ComplianceServiceRegulated::recordTransfer` runs `adjustInvestorsCountsByCountry("DE", "I_r", Increase)`: the EU branch at line 720 increments `euRetailInvestorsCount["DE"]` because the recipient is retail. The sender-side decrement skips because the sender is qualified.
- Final state: `euRetailInvestorsCount["DE"] = 51`, `euRetailInvestorsLimit = 50`. The cap is silently breached. Repeating the transfer to additional fresh retail addresses pushes the counter arbitrarily far above the configured cap.

The cap encodes a regulatory bound: per-country EU retail prospectus exemptions limit the number of retail-classified holders allowed in each member state. Once breached, the issuer is in violation of the exemption that the cap encodes in every affected jurisdiction; admitted retail investors hold tokens legally and the only remediation is the `onlyMaster` setter `setEURetailInvestorsCount(country, value)` at `contracts/compliance/ComplianceServiceRegulated.sol:878-882`, which resets the counter but does not unadmit anyone. The on-chain recovery primitive is therefore partial: it can stop further breaches but cannot reverse the regulatory non-compliance window that already occurred.

No malicious actor is required for the bypass to occur. Any deployment with both qualified investors holding token balances in an EU member state and active retail-investor onboarding in the same member state can silently breach the cap under routine transfer operations.

**Proof of Concept:** Add the following test to `test/solace-pocs/M-4.test.ts` and run with: `npx hardhat test test/solace-pocs/M-4.test.ts`.

```typescript
// PoC: EU retail cap skip clause over-extends to qualified senders.
// ComplianceServiceLibrary::completeTransferCheck at lines 340-350 (in
// contracts/compliance/ComplianceServiceRegulated.sol) rejects new retail
// admissions in EU country X when euRetailInvestorsCount[X] is at or above
// the cap, UNLESS the 4th conjunct evaluates to false.
//
// The 4th conjunct is meant to encode "no real offset is happening." The
// genuine offset case (per the increment-side logic at line 720) is:
// same country AND sender is retail AND sender depletes balance. In that
// case the recipient's +1 is matched by the sender's -1 on the same
// per-country counter, so the cap should permit the transfer.
//
// As written, the 4th conjunct is (!sameCountry || (fromBal > value AND
// isRetail(from))). The inner AND collapses to false whenever isRetail(from)
// is false, i.e., whenever the sender is qualified, even though a
// qualified sender never decrements euRetailInvestorsCount. So any
// qualified sender in country X can transfer tokens to a fresh retail
// recipient in country X past the per-country cap.
//
// The fix decouples the two predicates with OR (recommended in M-4 body):
//   (!sameCountry || !isRetail(from) || fromBal > value)
// so a qualified sender alone triggers conjunct-4 true and the cap fires.

import hre from 'hardhat';
import { expect } from 'chai';
import { loadFixture } from '@nomicfoundation/hardhat-toolbox/network-helpers';
import { deployDSTokenRegulated, INVESTORS } from '../utils/fixture';
import { DSConstants } from '../../utils/globals';

describe('PoC: completeTransferCheck EU retail cap skip clause over-extends to qualified senders', function () {
  it('test_PoC_QualifiedSenderBypassesEURetailCap', async function () {
    const [
      deployer,
      retailWallet1,
      retailWallet2,
      qualifiedWallet,
      freshRetailWallet,
    ] = await hre.ethers.getSigners();

    const {
      dsToken,
      registryService,
      complianceService,
      complianceConfigurationService,
    } = await loadFixture(deployDSTokenRegulated);

    // EU retail cap = 2 holders per EU country. Germany is configured EU.
    // Other limits are set wide so the only gate exercised in this PoC is
    // the EU retail cap.
    await complianceConfigurationService.setEURetailInvestorsLimit(2);
    await complianceConfigurationService.setNonAccreditedInvestorsLimit(100);
    await complianceConfigurationService.setTotalInvestorsLimit(100);
    await complianceConfigurationService.setMinEUTokens(0);
    await complianceConfigurationService.setMinimumHoldingsPerInvestor(0);
    await complianceConfigurationService.setCountryCompliance(
      INVESTORS.Country.GERMANY,
      INVESTORS.Compliance.EU,
    );

    // Step 1: onboard 2 retail Germans (no QUALIFIED attribute set) and
    // issue tokens to each. Each issuance increments
    // euRetailInvestorsCount["germany"] by 1 via adjustInvestorsCountsByCountry.
    // After step 1 the per-country counter sits at the cap: count = 2, limit = 2.
    await registryService.registerInvestor(
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_ID,
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_COLLISION_HASH,
    );
    await registryService.setCountry(
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_ID,
      INVESTORS.Country.GERMANY,
    );
    await registryService.addWallet(
      await retailWallet1.getAddress(),
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_ID,
    );
    await dsToken.issueTokens(await retailWallet1.getAddress(), 100n);

    await registryService.registerInvestor(
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_ID_2,
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_COLLISION_HASH_2,
    );
    await registryService.setCountry(
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_ID_2,
      INVESTORS.Country.GERMANY,
    );
    await registryService.addWallet(
      await retailWallet2.getAddress(),
      INVESTORS.INVESTOR_ID.GERMANY_INVESTOR_ID_2,
    );
    await dsToken.issueTokens(await retailWallet2.getAddress(), 100n);

    expect(
      await complianceService.getEURetailInvestorsCount(INVESTORS.Country.GERMANY),
    ).to.equal(2n);

    // Step 2: onboard a QUALIFIED German investor with token balance.
    // Qualified investors do not increment euRetailInvestorsCount: the EU
    // branch in adjustInvestorsCountsByCountry (line 720) is gated on
    // !isQualifiedInvestor.
    const qualifiedId = 'germanyQualifiedInvestorId';
    await registryService.registerInvestor(qualifiedId, 'germanyQualifiedInvestorCollisionHash');
    await registryService.setCountry(qualifiedId, INVESTORS.Country.GERMANY);
    await registryService.setAttribute(
      qualifiedId,
      DSConstants.attributeType.QUALIFIED,
      DSConstants.attributeStatus.APPROVED,
      0,
      'qualification-proof',
    );
    await registryService.addWallet(await qualifiedWallet.getAddress(), qualifiedId);
    await dsToken.issueTokens(await qualifiedWallet.getAddress(), 200n);

    // Retail counter unchanged: the qualified investor is not counted.
    expect(
      await complianceService.getEURetailInvestorsCount(INVESTORS.Country.GERMANY),
    ).to.equal(2n);

    // Step 3: register a FRESH retail German with NO token balance. The
    // investor is registered but has not yet been counted (no issuance has
    // happened on them).
    const freshRetailId = 'germanyFreshRetailInvestorId';
    await registryService.registerInvestor(freshRetailId, 'germanyFreshRetailInvestorCollisionHash');
    await registryService.setCountry(freshRetailId, INVESTORS.Country.GERMANY);
    await registryService.addWallet(await freshRetailWallet.getAddress(), freshRetailId);

    // Sanity: issuing tokens DIRECTLY to the fresh retail German is correctly
    // rejected by preIssuanceCheck's EU retail cap. The bypass is specific
    // to completeTransferCheck (the transfer path), not preIssuanceCheck
    // (the issuance path).
    await expect(
      dsToken.issueTokens(await freshRetailWallet.getAddress(), 100n),
    ).to.be.revertedWith('Max investors in category');

    // BUG: transfer from the qualified German to the fresh retail German
    // bypasses the EU retail cap. The 4th conjunct in completeTransferCheck
    // evaluates as:
    //   !sameCountry || (fromBal > value && isRetail(from))
    //   = !isEqualString("germany", "germany") || (200 > 100 && false)
    //   = false || (true && false)
    //   = false
    // With conjunct 4 false, the four-conjunct REJECT predicate is false
    // and the cap rejection does not fire. The transfer succeeds.
    await expect(
      dsToken
        .connect(qualifiedWallet)
        .transfer(await freshRetailWallet.getAddress(), 100n),
    ).to.not.be.reverted;

    // BUG ASSERTION: euRetailInvestorsCount["germany"] is now 3, breaching
    // the configured cap of 2. The fresh retail German was admitted past
    // the cap without any offsetting decrement.
    expect(
      await complianceService.getEURetailInvestorsCount(INVESTORS.Country.GERMANY),
    ).to.equal(3n);

    // Balances confirm the transfer actually happened.
    expect(await dsToken.balanceOf(await qualifiedWallet.getAddress())).to.equal(100n);
    expect(await dsToken.balanceOf(await freshRetailWallet.getAddress())).to.equal(100n);
  });
});
```

Test result on the unfixed codebase:

```
PoC: completeTransferCheck EU retail cap skip clause over-extends to qualified senders
  ✔ test_PoC_QualifiedSenderBypassesEURetailCap (1255ms)

1 passing (1s)
```

The test reproduces the bug end-to-end under normal Issuer operations with no malicious actor required. The cap is configured at 2 retail Germans, filled to the limit via two retail-German issuances, and the qualified-sender transfer to a fresh retail German breaches the cap by admitting the new retail recipient past the limit. The sanity step (`issueTokens` directly to the fresh retail German is correctly rejected) confirms that the bypass is specific to the transfer path's `completeTransferCheck` and not a generalized cap misconfiguration.

**Recommended Mitigation:** Two options. Option A is the minimal one-line fix; Option B is the preferred structural refactor.

**Option A (minimal fix).** Replace the skip clause at line 347 to mirror the US-accredited cap's structure at line 381. Change:

```solidity
(!CommonUtils.isEqualString(getCountry(_services, _args.from), toCountry) ||
 (_args.fromInvestorBalance > _args.value && isRetail(_services, _args.from)))
```

to:

```solidity
(!CommonUtils.isEqualString(getCountry(_services, _args.from), toCountry) ||
 !isRetail(_services, _args.from) ||
 _args.fromInvestorBalance > _args.value)
```

Inverted, the cap now correctly skips only when `same country AND sender is retail AND sender depletes balance`, which is exactly the case where the `+1` retail recipient is offset by a `-1` retail decrement on the sender, matching the increment-side logic at line 720.

**Option B (structural refactor, preferred).** The root cause of this bug is that the cap-rejection predicate is a four-conjunct compound expression with a nested OR-of-AND in the carve-out leg. Compound boolean predicates with mixed AND/OR nesting are a known anti-pattern: each named precondition gets buried inside an expression tree, the polarity of every sub-predicate has to be tracked mentally, and a single inverted operator (`fromBal > value` vs `fromBal <= value`, or `AND` vs `OR`) produces a silently-wrong predicate that still type-checks and still passes the happy-path tests. The fix should not stop at correcting the single inverted clause, it should also restructure the cap check so the same shape of bug is not reachable by any future maintainer.

Extract the cap-rejection logic into a named helper function with one named local per precondition and an early-return for each one. The same refactor applies to the four sibling cap branches in `completeTransferCheck` (JP at lines 330-339, US at 366-373, US-accredited at 376-384, total-investors at 399-407) and to the mirror sites in `preIssuanceCheck` at lines 487-520. Worked example for the EU retail cap:

```solidity
function _wouldBreachEURetailCap(
    address[] memory _services,
    CompletePreTransferCheckArgs memory _args,
    string memory toCountry,
    uint256 toInvestorBalance
) internal view returns (bool) {
    // Cap applies only when the recipient would be newly admitted as retail.
    bool recipientIsNewRetail =
        isRetail(_services, _args.to) && isNewInvestor(toInvestorBalance);
    if (!recipientIsNewRetail) {
        return false;
    }

    // Cap applies only when the per-country counter is at or above the limit.
    uint256 limit = IDSComplianceConfigurationService(
        _services[COMPLIANCE_CONFIGURATION_SERVICE]
    ).getEURetailInvestorsLimit();
    uint256 current = ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE])
        .getEURetailInvestorsCount(toCountry);
    if (limit == 0 || current < limit) {
        return false;
    }

    // The recipient's +1 retail admission is offset only when the sender is
    // a retail depleter in the same country (-1 retail decrement on the
    // same per-country counter). Any other sender shape (different country,
    // qualified, or retail retainer) leaves the counter to grow past the cap.
    bool sameCountry = CommonUtils.isEqualString(
        getCountry(_services, _args.from),
        toCountry
    );
    bool senderIsRetailDepleter =
        sameCountry &&
        isRetail(_services, _args.from) &&
        _args.fromInvestorBalance == _args.value;
    return !senderIsRetailDepleter;
}
```

The call site at line 340-350 then reduces to:

```solidity
} else if (toRegion == EU) {
    if (_wouldBreachEURetailCap(_services, _args, toCountry, toInvestorBalance)) {
        return (40, MAX_INVESTORS_IN_CATEGORY);
    }
    if (toInvestorBalance + _args.value < IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getMinEUTokens()) {
        return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
    }
}
```

Three properties this refactor buys that the inline expression does not:

1. Each precondition has a name and a comment explaining its role. The polarity of every sub-predicate is local to one line, not buried in a compound expression. A reviewer scanning `senderIsRetailDepleter = sameCountry && isRetail(_args.from) && _args.fromInvestorBalance == _args.value` reads the offset condition verbatim and can verify it against the increment-side logic at line 720 in one glance.
2. The cap check folds the `limit == 0` guard that a separate finding documents, closing the missing-`!= 0`-guard regression by construction rather than by remembering to add the guard at every cap-check site.
3. The function is testable in isolation. The current inline compound predicate has to be exercised via the full `completeTransferCheck` call path, which makes property-style testing (enumerate all sender-shape combinations, assert cap-rejection matches the offset definition) awkward. A standalone `_wouldBreachEURetailCap` is a pure view function that fuzz tests can saturate quickly.

The same refactor pattern applies verbatim to the sibling cap branches; restructuring all five caps (JP, EU retail, US, US-accredited, total-investors) and their `preIssuanceCheck` mirrors as named helpers eliminates the entire class of "compound cap predicate with subtly wrong polarity" bug that this finding exemplifies.

**Securitize:** Fixed in [56c3eff](https://github.com/securitize-io/dstoken/commit/56c3eff49d1f3173824bf23a699c027be043cc2c).

**Cyfrin:** Verified.
