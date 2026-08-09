---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: Legacy retail template is copied into category 45 with no validation of percentage
  or end timestamp
vuln_class: []
---

# Legacy retail template is copied into category 45 with no validation of percentage or end timestamp

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** The deploy script reads the existing template from category 1 and copies it verbatim into category 45 at index 0, then appends the new `2 + 2` template at index 1. The only validation is that exactly one old template exists.

```ts
//deploy-wlfi-v3-updates.ts#L148-L181
const oldTemplates = await vesterProxy.getAllCategoryTemplates(1);
if (oldTemplates.length !== 1) {
  throw new Error('Expected old templates to have length 1');
}

transactions.push(
  // Bring over the old template
  await prettyPrintEncodedDataWithTypeSafety(
    core,
    'WorldLibertyFinancialVester',
    vesterProxy.ownerSetCategoryTemplate,
    [
      FinalizedVestingCategory.RETAIL, 0, {
      percentageOfAllocation: oldTemplates[0].percentageOfAllocation,
      startTimestamp: oldTemplates[0].startTimestamp,
      cliffTimestamp: oldTemplates[0].cliffTimestamp,
      endTimestamp: oldTemplates[0].endTimestamp,
    },
    ],
  ),
  // Put in 2 + 2
  await prettyPrintEncodedDataWithTypeSafety(
    core,
    'WorldLibertyFinancialVester',
    vesterProxy.ownerSetCategoryTemplate,
    [
      FinalizedVestingCategory.RETAIL, 1, {
      percentageOfAllocation: parseEther(`${0.8}`),
      startTimestamp: VESTING_START_TIMESTAMP,
      cliffTimestamp: VESTING_START_TIMESTAMP,
      endTimestamp: VESTING_START_TIMESTAMP + TWO_YEARS_IN_SECONDS,
    },
    ],
  ),
```

The vester walks templates in order, capping each segment by the remaining allocation:

```solidity
//WorldLibertyFinancialVester.sol#L298-L336
function _unlockedTotal(
    VesterStorage storage $,
    uint8 _category,
    uint112 _allocation
) internal view returns (uint256) {
    ...
    for (uint8 i; i < count; ) {
        Template memory template = $.categoryTemplates[_category][i];

        uint256 segmentCap = _allocation * uint256(template.percentageOfAllocation) / MAX_PERCENTAGE;
        segmentCap = segmentCap < remainingCap ? segmentCap : remainingCap;
        ...
    }
    return totalUnlocked;
}
```

The behavior of category 45 after deployment depends on three properties of `oldTemplates[0]` that the script never asserts:

1. `percentageOfAllocation`. If `oldTemplates[0].percentageOfAllocation + 0.8 ether > 1 ether`, template 1 is silently capped by `remainingCap` and unlocks less than 80% of allocation. If `oldTemplates[0].percentageOfAllocation == 0`, only 80% of allocation ever vests through category 45, and 20% becomes permanently unreachable through this category.
2. `endTimestamp`. If `oldTemplates[0].endTimestamp > VESTING_START_TIMESTAMP`, the post-election retail schedule is a hybrid of the legacy curve and the new 2-year curve, not the proposal's clean "2-year cliff + 2-year linear" curve.
3. `cliffTimestamp` relative to `block.timestamp`. If the old template was configured with `start < cliff`, it interacts with the phantom-unlock issue described in M-02 of this audit.

The script does not print `oldTemplates[0]` and the multisig signers have no opportunity to eyeball it before approving the bundle.

**Impact:** The script's correctness for the retail cohort is fully delegated to whatever happens to be stored at `categoryTemplates[1][0]` on mainnet at deployment time. If that template diverges from the assumed shape, the post-election retail vesting curve quietly diverges from the proposal in a way that is not visible from the script source, the proposal text, or the `invariants` block. The most material divergence is silent capping: a template 0 with `percentageOfAllocation > 0.2 ether` causes template 1 to be capped at `1 ether - oldPct`, so retail receives less than the advertised 80% on the new schedule.

**Proof of Concept:**
```
Assume mainnet category 1 currently holds:
  oldTemplates[0] = {
    percentageOfAllocation: 0.5 ether,    // 50%
    startTimestamp:        someTime,
    cliffTimestamp:        someTime,
    endTimestamp:          someTimeInPast
  }

After the script runs, category 45 holds:
  index 0 = oldTemplates[0]                   // 50% allocation, fully unlocked
  index 1 = { 0.8 ether, VESTING_START, ... } // intends 80% over 2y

For a user with allocation = 1000 WLFI:
  remainingCap starts at 1000.
  index 0: segmentCap = 1000 * 0.5 = 500. Already past endTimestamp, fully unlocked.
           remainingCap -= 500 -> 500.
  index 1: segmentCap = 1000 * 0.8 = 800, capped to remainingCap = 500.
           Linear from VESTING_START over 2y, max 500 WLFI.

Effective curve: 500 WLFI immediately claimable post-election, 500 WLFI over 2y.
Proposal curve: 0 immediately, then linear to 800 WLFI over 2y, with the
remaining 200 (old template) already accounted for in claimed.

The old percentage is unknown to anyone reading this script in isolation,
so the deviation is invisible.
```

**Recommended Mitigation:** Add explicit assertions in the script before the template copy, with concrete expected values pulled from the on-chain state of `categoryTemplates[1][0]` at the time the proposal was drafted. For example:

```ts
const old = oldTemplates[0];
if (old.percentageOfAllocation !== EXPECTED_LEGACY_RETAIL_PCT) {
  throw new Error(`Unexpected legacy retail percentage: ${old.percentageOfAllocation}`);
}
if (old.endTimestamp > VESTING_START_TIMESTAMP) {
  throw new Error(`Legacy retail template still active past VESTING_START`);
}
if (old.percentageOfAllocation + parseEther('0.8') > parseEther('1')) {
  throw new Error('Legacy retail percentage + new 80% exceeds 100%');
}
```

Also extend the `invariants` block to print and assert the resulting `categoryTemplates[45]` shape so the multisig has a final on-chain check before the bundle executes.

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
