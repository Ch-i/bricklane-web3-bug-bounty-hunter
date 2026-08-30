---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-04] `StakingOperation` will drip rewards to no-one if rewards are queued
  before any deposit'
vuln_class: []
---

# [L-04] `StakingOperation` will drip rewards to no-one if rewards are queued before any deposit

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

I believe they will have modest losses until someone deposits

This is further corroborated by the fact that the first deposit will continue instead of going through the early return path

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/StakingOperations.sol#L219-L230

```solidity
  function updatePool(ISwapPair _pid) public {
    PoolInfo storage pool = poolInfo[_pid];

    // check
    if (block.timestamp <= pool.lastRewardTime) return;

    // update
    uint tokenSupply = _pid.balanceOf(address(this));
    if (tokenSupply == 0 || totalAllocPoint == 0) {
      pool.lastRewardTime = block.timestamp;
      return;
    }
```

**Mitigation**

Simply delay the first emission by a few hours or days to ensure someone has staked
