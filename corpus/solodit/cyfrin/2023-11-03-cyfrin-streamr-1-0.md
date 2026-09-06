---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: In `VoteKickPolicy.onFlag()`, `targetStakeAtRiskWei[target]` might be greater
  than `stakedWei[target]` and `_endVote()` would revert.
vuln_class: []
---

# In `VoteKickPolicy.onFlag()`, `targetStakeAtRiskWei[target]` might be greater than `stakedWei[target]` and `_endVote()` would revert.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** Medium

**Description:** `targetStakeAtRiskWei[target]` might be greater than `stakedWei[target]` in `onFlag()`.

```solidity
targetStakeAtRiskWei[target] = max(stakedWei[target], streamrConfig.minimumStakeWei()) * streamrConfig.slashingFraction() / 1 ether;
```

For example,
- At the first time, `streamrConfig.minimumStakeWei() = 100` and an operator(=target) has staked 100.
- `streamrConfig.minimumStakeWei()` was increased to 2000 after a reconfiguration.
- `onFlag()` is called for target and `targetStakeAtRiskWei[target]` will be `max(100, 2000) * 10% = 200`.
- In `_endVote()`, `slashingWei = _kick(target, slashingWei)` will be 100 because target has staked 100 only.
- So it will revert due to underflow during the reward distribution.

**Impact:** Operators with small staked funds wouldn't be kicked forever.

**Recommended Mitigation:** `onFlag()` should check if a target has staked enough funds for rewards and handle separately if not.

**Client:** Fixed in commit [05d9716](https://github.com/streamr-dev/network-contracts/commit/05d9716b8e19668fea70959327ab8e896ab0645d). Flag targets with not enough stake (to pay for the review) will be kicked out without review. Since this can only happen after the admin changes the minimum stake requirement (e.g. by increasing reviewer rewards), the flag target is not at fault and will not be slashed. They can stake back again with the new minimum stake if they want.

**Cyfrin:** Verified.
