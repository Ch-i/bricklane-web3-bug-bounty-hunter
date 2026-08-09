---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-1-4
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
title: Team election to category 47 discards the user's prior vesting templates and
  creates a post-election claim blackout
vuln_class: []
---

# Team election to category 47 discards the user's prior vesting templates and creates a post-election claim blackout

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** The retail path of `_electVestingUpdate` preserves the user's previous vesting by copying the old category-1 template into category 45 at index 0 before the new 2-year template is appended at index 1. The team path does not. After election, a category-47 user has a single template covering 100% of their (post-burn) allocation linearly from `VESTING_START_TIMESTAMP` to `VESTING_START_TIMESTAMP + THREE_YEARS_IN_SECONDS`, with no carryover of the prior schedule.

`UserInfo.claimed` is preserved across the category switch. Claimable amount in the vester is `unlocked - claimed`:

```solidity
//WorldLibertyFinancialVester.sol#L285-L295
function _claimable(
    VesterStorage storage $,
    UserInfo memory _userInfo
) internal view returns (uint256) {
    if (!_userInfo.initialized) {
        return 0;
    }

    uint256 unlocked = _unlockedTotal($, _userInfo.category, _userInfo.allocation);
    return unlocked > _userInfo.claimed ? unlocked - _userInfo.claimed : 0;
}
```

The deploy script wires up the asymmetry: category 45 keeps the old template plus the new one, while category 47 only sets one template.

```ts
//deploy-wlfi-v3-updates.ts#L153-L196
// Bring over the old template
vesterProxy.ownerSetCategoryTemplate,
[
  FinalizedVestingCategory.RETAIL, 0, {
  percentageOfAllocation: oldTemplates[0].percentageOfAllocation,
  startTimestamp: oldTemplates[0].startTimestamp,
  cliffTimestamp: oldTemplates[0].cliffTimestamp,
  endTimestamp: oldTemplates[0].endTimestamp,
},
],
// Put in 2 + 2
vesterProxy.ownerSetCategoryTemplate,
[
  FinalizedVestingCategory.RETAIL, 1, {
  percentageOfAllocation: parseEther(`${0.8}`),
  startTimestamp: VESTING_START_TIMESTAMP,
  cliffTimestamp: VESTING_START_TIMESTAMP,
  endTimestamp: VESTING_START_TIMESTAMP + TWO_YEARS_IN_SECONDS,
},
],
// Put in 2 + 3, all allocation
vesterProxy.ownerSetCategoryTemplate,
[
  FinalizedVestingCategory.TEAM, 0, {
  percentageOfAllocation: parseEther(`${1}`),
  startTimestamp: VESTING_START_TIMESTAMP,
  cliffTimestamp: VESTING_START_TIMESTAMP,
  endTimestamp: VESTING_START_TIMESTAMP + THREE_YEARS_IN_SECONDS,
},
],
```

For any team-cohort user who was previously activated and has `claimed > 0` under their old category template, election produces:

- `allocation_new = 0.9 * allocation_old`
- `claimed` unchanged
- `unlocked_new(t) = 0.9 * allocation_old * (t - VESTING_START) / 3y`, clamped to `[0, 0.9 * allocation_old]`
- `claimable_new = max(0, unlocked_new(t) - claimed)`

`claimable_new` stays at 0 until `0.9 * allocation_old * (t - VESTING_START) / 3y > claimed`, i.e. for roughly `3y * claimed / (0.9 * allocation_old)` after the cliff. A team user who had already claimed 10% of their pre-burn allocation faces a ~4-month blackout past `VESTING_START` before any new claim succeeds.

**Impact:** The proposal advertises a 2-year cliff followed by a 3-year linear vest for the team cohort. For team users who claimed any tokens under their previous category, the actual post-election schedule is later than that: claims do not resume at the cliff, they resume only after the new linear curve has caught up to the user's already-claimed amount. This is not disclosed in the proposal text, is not exercised by the script's `invariants` block (which uses a team user with `claimed = 0`), and is asymmetric with the retail design that explicitly carries the old template forward to avoid this exact effect.

The asymmetry also means the proposal's "10% burn + 3-year linear" description is slightly misleading: a team user with prior claims effectively receives less than 90% of their tokens over the 3-year window because the early portion is consumed by their existing `claimed`. Allocation accounting is correct in aggregate, but the user-visible claim curve is not the one the proposal describes.

**Proof of Concept:** Steps with concrete numbers:

```
1. Pre-election (in category 18, e.g.):
   - allocation = 1000 WLFI
   - claimed    = 100 WLFI (user previously claimed 10% under old schedule)
2. Owner calls ownerElectVestingUpdatesFor([user]) at any time before VESTING_START.
   - Burn 10%: allocation -> 900 WLFI (assert claimed <= allocation passes: 100 <= 900)
   - Category set to 47 in both vester and registry.
3. At VESTING_START (cliff): unlocked = 0 (start == cliff, elapsed = 0).
   claimable = max(0, 0 - 100) = 0.
4. At VESTING_START + 4 months: unlocked = 900 * (4/36) = 100 WLFI.
   claimable = max(0, 100 - 100) = 0. Still cannot claim.
5. At VESTING_START + 4 months + 1 day: unlocked just exceeds 100, claimable becomes
   non-zero. The user only now starts seeing claims, despite the cliff having passed.
```

The retail flow does not exhibit this because template 0 of category 45 is the old template, so the previously-vested chunk that produced `claimed` is still represented in `unlocked` after election.

**Recommended Mitigation:** Either preserve the prior team template the same way retail does, or refuse to elect when the new schedule would produce `unlocked < claimed` at `VESTING_START`.

Preserving the prior template requires the script to read the user's previous category templates per legacy team category and copy them into category 47 alongside the new template. Because team users span multiple legacy categories (2 through 20), this is not a single template copy and may require category 47 to be split or for templates to be set per-user, which is incompatible with the current shared-category model.

A simpler fix is to enforce the precondition in `_electVestingUpdate`:

```solidity
if (newCategory == 47) {
    uint256 allocation = VESTER.allocation(_account);
    uint256 amountToBurn = allocation / 10;
    uint256 newAllocation = allocation - amountToBurn;
    uint256 alreadyClaimed = VESTER.claimed(_account);
    if (alreadyClaimed > 0) {
        revert TeamElectionWouldBlackoutClaims(_account, alreadyClaimed);
    }
    VESTER.wlfiBurnAllocation(_account, amountToBurn);
    REGISTRY.wlfiBurnAllocation(_account, amountToBurn);
}
```

Equivalently, document the blackout behavior and add an invariant that asserts no team user with `claimed > 0` is elected during deployment. The script's existing `invariants` block should add a case that pre-claims under a team category and then asserts the post-election claim trajectory.

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
