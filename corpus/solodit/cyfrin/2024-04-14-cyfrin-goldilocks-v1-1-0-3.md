---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-0-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Team members can't unstake the initial allocation forever.
vuln_class: []
---

# Team members can't unstake the initial allocation forever.

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** High

**Description:** When users call `unstake()`, it calculates the vested amount using `_vestingCheck()`.

```solidity
  function _vestingCheck(address user, uint256 amount) internal view returns (uint256) {
    if(teamAllocations[user] > 0) return 0; //@audit return 0 for team members
    uint256 initialAllocation = seedAllocations[user];
    if(initialAllocation > 0) {
      if(block.timestamp < vestingStart) return 0;
      uint256 vestPortion = FixedPointMathLib.divWad(block.timestamp - vestingStart, vestingEnd - vestingStart);
      return FixedPointMathLib.mulWad(vestPortion, initialAllocation) - (initialAllocation - stakedLocks[user]);
    }
    else {
      return amount;
    }
  }
```

But it returns 0 for team members and they can't unstake forever.
Furthermore, in `stake()`, it just prevents seed investors, not team members. So if team members have staked additionally, they can't unstake also.

**Impact:** Team members can't unstake forever.

**Recommended Mitigation:** `_vestingCheck` should use the same logic as initial investors for team mates.

**Client:** Acknowledged, it is intended that the team cannot unstake their tokens. [PR #4](https://github.com/0xgeeb/goldilocks-core/pull/4) fixes issue of `stake` not preventing team members from staking.

**Cyfrin:** Verified.
