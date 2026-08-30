---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-topiastaking-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-topiastaking
title: '[L-01] Precision loss due to division before multiplication'
vuln_class: []
---

# [L-01] Precision loss due to division before multiplication

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-TopiaStaking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md)_

---

The `estimateStakeReward` method does division before multiplication, which would lead to unnecessary precision loss in Solidity. This will result in incorrect estimation on the front-end for users that want to see a reward projection, showing less than it should have. Make the code so that multiplication comes before division.

**Discussion**

**pashov:** Fixed.
