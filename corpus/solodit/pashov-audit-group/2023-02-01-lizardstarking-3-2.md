---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[L-03] Unexpected behavior if user stakes in the same block as when the first
  pool is created'
vuln_class: []
---

# [L-03] Unexpected behavior if user stakes in the same block as when the first pool is created

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

If there is only 1 rewards pool and a user has staked in exactly the same block as when the pool was created, then both

```solidity
(pool[pool.length - 1].time) <= timeLizardLocked[_tokenId]
```

and

```solidity
timeLizardLocked[_tokenId] <= pool[0].time
```

will return `true`. The problem is the first check is in the `if` of `getCurrentShareRaw`, while the second one is in the `else if`, and depending on which branch the code takes different calculations happen for the share amount. Removing the `=` sign from either of them will fix the issue, where I would say it is more correct to remove it in the `if` statement, as it is fair that a user that staked in the same block gets the shares inflation of the pool.

There is also another problem that is very close to this one: in `getCurrentShareRaw` if a user stakes in the same `block.timestamp` as when the first pool is created, then his share will be calculated as if he is included in that first pool. This is not the case for the `claimCalculation` function, where if the user has staked in the same block (same `block.timestamp`) where the first pool was created, his rewards won't include the rewards from the first block. This is unexpected as the protocol doesn't document this behavior is intended - receiving the pool's share inflation but not receiving the pool's rewards when you stake in the same block as when the first pool was created.

My recommendation is that the user should receive both inflation and rewards for his stake if he staked in the same block as when a pool was created, think through this in depth.
