---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[M-01] Some vesting recipients temporarily won''t be able to claim'
vuln_class: []
---

# [M-01] Some vesting recipients temporarily won't be able to claim

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

**Impact:**
Medium, as funds will be locked for 30 days

**Likelihood:**
Medium, because it will only happen when the cliff is < 30 day

**Description**

The `SLICE_PERIOD` constant in `Vesting` is set to 30 days. Due to the following math in `_computeReleasableAmount`

```solidity
uint256 vestedSeconds = (timeFromStart / SLICE_PERIOD) * SLICE_PERIOD;
```

If `timeFromStart` is less than 30 days this will round down to zero, which means the amount to claim until 30 days have passed will always be zero. This applies especially for vesting schedules that have no `cliff` (it is 0), which is expected for `Investors` and `Treasury`.

**Recommendations**

Make the `SLICE_PERIOD` smaller, or implement another design for handling no cliff vesting schedules that won't be using this calculation.
