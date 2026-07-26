---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: Linear vesting accrues from `startTimestamp` instead of `cliffTimestamp`, causing
  a phantom unlock at the cliff when `start < cliff`
vuln_class: []
---

# Linear vesting accrues from `startTimestamp` instead of `cliffTimestamp`, causing a phantom unlock at the cliff when `start < cliff`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `_segmentUnlocked` computes the linear unlock as a fraction of `(currentTimestamp - startTimestamp) / (endTimestamp - startTimestamp)`. The pre-cliff branch returns `0` while `currentTimestamp < cliffTimestamp`, but the linear schedule itself is anchored at `startTimestamp`, not `cliffTimestamp`.

```solidity
//WorldLibertyFinancialVester.sol#L339-L365
function _segmentUnlocked(Template memory _template, uint256 _segmentCap) internal view returns (uint256) {
    assert(_segmentCap != 0);

    uint32 currentTimestamp = uint32(block.timestamp);

    if (_template.endTimestamp == 0) {
        return _segmentCap;
    }
    if (currentTimestamp < _template.cliffTimestamp) {
        return 0;
    }
    if (currentTimestamp >= _template.endTimestamp) {
        return _segmentCap;
    }

    uint256 elapsed = uint256(currentTimestamp) - uint256(_template.startTimestamp);
    uint256 span = uint256(_template.endTimestamp) - uint256(_template.startTimestamp);

    assert(span != 0);

    return (_segmentCap * elapsed) / span;
}
```

The template setter at `ownerSetCategoryTemplate` only enforces the ordering `startTimestamp <= cliffTimestamp <= endTimestamp`, so any template with `start < cliff` is accepted, and the interface explicitly documents the schedule as `linear from (startTimestamp -> endTimestamp); cliffTimestamp must be greater than or equal to startTimestamp`:

```solidity
//WorldLibertyFinancialVester.sol#L49-L81
function ownerSetCategoryTemplate(
    uint8 _category,
    uint8 _index,
    Template calldata _template
) external onlyWorldLibertyOwner(msg.sender) {
    if (_index >= MAX_TEMPLATE_COUNT) {
        revert InvalidTemplateCount();
    }
    if (_template.endTimestamp != 0) {
        if (
            _template.startTimestamp > _template.cliffTimestamp
            || _template.cliffTimestamp > _template.endTimestamp
        ) {
            revert InvalidTemplateTimestamp();
        }
    }
    ...
}
```

When `start < cliff`, accrual silently builds between `start` and `cliff` while the pre-cliff guard hides it. The instant `block.timestamp` reaches `cliff`, `_claimable` jumps from `0` to `segmentCap * (cliff - start) / (end - start)` in a single block.

**Impact:** The proposal language for early-supporter style allocations reads as `2-year cliff, then 2-year linear vest, tokens beginning to unlock at year 2 and fully distributed by year 4`. The intuitive template configuration for that schedule is `start = electionTime`, `cliff = start + 2y`, `end = start + 4y`. With the current math the user receives `50%` of their allocation in the same block the cliff is crossed, instead of unlocking smoothly from `0%` at year 2 to `100%` at year 4. After 1 year past the cliff the user holds `75%` instead of the spec's `50%`.

The bug is dormant only as long as every template is configured with `start == cliff`. Nothing in the contract enforces that invariant and the interface docs explicitly allow `start < cliff`. Any team category created with the proposal's natural reading distributes more tokens earlier than the proposal's vesting curve and increases circulating supply ahead of schedule.

**Proof of Concept:** The following test was added to `test/wlfi/WorldLibertyFinancialVester.test.ts` as part of this audit and passes against the current code on a fork at block `23_200_000`.

Result on the current code:
```
WorldLibertyFinancialVester
  Edge Cases and Branch Coverage
    _segmentUnlocked
      Resetting hardhat fork for network ethereum...
      PHANTOM UNLOCK: jumps to 50% of allocation at cliff time when start < cliff

1 passing
```

The body of the PoC pins down the buggy values directly. Schedule under test: `start = electionTime`, `cliff = start + 2y`, `end = start + 4y`, allocation `100 WLFI`, single template at `100%`:

```typescript
const start = WLFI_START_TIMESTAMP;
const cliff = WLFI_START_TIMESTAMP + TWO_YEARS_S;   // start + 2y
const end   = WLFI_START_TIMESTAMP + FOUR_YEARS_S;  // start + 4y
...
// Just before cliff: pre-cliff guard returns 0, as expected.
await time.increaseTo(cliff - 1n);
expect(await ctx.vester.claimable(ctx.core.hhUser1)).to.eq(0);

// AT cliff: spec implies 0% (start of linear). Bug returns 50%.
await time.increaseTo(cliff);
expect(await ctx.vester.claimable(ctx.core.hhUser1)).to.eq(amount / 2n);

// 1 year past cliff: spec says 50% (halfway through 2y linear). Bug returns 75%.
await time.increaseTo(cliff + (TWO_YEARS_S / 2n));
expect(await ctx.vester.claimable(ctx.core.hhUser1)).to.eq((amount * 3n) / 4n);
```

**Recommended Mitigation:** Anchor the linear schedule at `cliffTimestamp` so the cliff actually marks the start of vesting, not just a claim gate over a schedule that has been silently accruing since `startTimestamp`:

```diff
-        uint256 elapsed = uint256(currentTimestamp) - uint256(_template.startTimestamp);
-        uint256 span = uint256(_template.endTimestamp) - uint256(_template.startTimestamp);
+        uint256 elapsed = uint256(currentTimestamp) - uint256(_template.cliffTimestamp);
+        uint256 span = uint256(_template.endTimestamp) - uint256(_template.cliffTimestamp);
```

The `assert(span != 0)` invariant still holds: the pre-cliff guard plus the `currentTimestamp >= endTimestamp` early return together imply `cliff <= currentTimestamp < endTimestamp` at the point the assertion runs, hence `endTimestamp > cliffTimestamp` and `span > 0`. Reflipping the test assertions noted in the PoC test to `0` at cliff and `amount / 2n` at cliff + 1y after the fix is sufficient to lock the new behavior in.

If the team wants to preserve the option of templates whose linear schedule predates the cliff (so that the cliff intentionally releases a precomputed chunk), enforce `startTimestamp == cliffTimestamp` in `ownerSetCategoryTemplate` and update the interface docs accordingly, so the API can no longer be configured into the buggy regime.

**WLFI:** Acknowledged. This is expected behavior. To mitigate this, we purposefully set `startTimestamp == cliffTimestamp` when we want to avoid this behavior.
