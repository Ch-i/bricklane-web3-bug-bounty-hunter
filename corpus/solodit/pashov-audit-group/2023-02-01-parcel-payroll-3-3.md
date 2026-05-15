---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-3-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[I-04] Inconsistency in file header comments'
vuln_class: []
---

# [I-04] Inconsistency in file header comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

Most files in the codebase have a comment on the first line of the file that looks like

```solidity
//contracts/Organizer.sol
```

The problem is that some files have it, while others don't, which is inconsistent. Those comments shouldn't really be needed anyway so it's best to remove them altogether from the codebase and if not - add the correct comment to each separate smart contract file.
