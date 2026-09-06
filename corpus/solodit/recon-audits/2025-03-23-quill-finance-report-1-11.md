---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-11
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-12] `ETH_GAS_COMPENSATION` changes may cause unprofitable liquidations
  during gas fees spikes - Suggested changes'
vuln_class: []
---

# [L-12] `ETH_GAS_COMPENSATION` changes may cause unprofitable liquidations during gas fees spikes - Suggested changes

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The variable `ETH_GAS_COMPENSATION` in Quill was changed to:

```solidity
// Amount of ETH to be locked in gas pool on opening troves
uint256 constant ETH_GAS_COMPENSATION = 0.001 ether;
```

This can be insufficient for liquidations that happen at a high GWEI

**Data**

From these pages we can see that sometimes the gas can spike up to 3 GWEI on Rollups

https://scrollscan.com/chart/gasprice
https://blastscan.io/chart/gasprice
https://optimistic.etherscan.io/chart/gasprice


**Math**

This is taken off of the Tests provided in the repo

```
| batchLiquidateTroves                                                        | 30566           | 714168 | 648149 | 9548229 | 221     |
| liquidate                                                                   | 76475           | 468522 | 389065 | 727942  | 4796    |
```

```python
>>> ASSUMED_WORST_CASE_LIQUIDATION_COST = 350_000
>>> ASSUMED_WORST_CASE_LIQUIDATION_COST * 2e9 / 1e18
0.0007
>>> ASSUMED_WORST_CASE_LIQUIDATION_COST * 3e9 / 1e18
0.00105
```

```python
>>> ASSUMED_WORST_CASE_LIQUIDATION_COST = 800_000
>>> ASSUMED_WORST_CASE_LIQUIDATION_COST * 2e9 / 1e18
0.0016
>>> ASSUMED_WORST_CASE_LIQUIDATION_COST * 3e9 / 1e18
0.0024
>>> ASSUMED_WORST_CASE_LIQUIDATION_COST * 100e9 / 1e18
0.08
```


**Mitigation**

Perform more in depth benchmarks
And determine if the dynamic collateral premium is sufficient


Am thinking

ASSUMED_WORST_CASE_LIQUIDATION_COST = 350_000
ASSUMED_WORST_CASE_LIQUIDATION_COST * 10e9 / 1e18
0.0035

Which is $12 

Is probably a good point to shot at

Past that MEV actors should generally be able to optimize their gas cost
And 1/20 for min size also seems like it's not too burdensome to users
