---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[L-06] Code naming gives an assumption that is not enforced'
vuln_class: []
---

# [L-06] Code naming gives an assumption that is not enforced

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The `allowedContracts` mapping can contain EOAs as well as contracts in it. Another dev can expect only contracts to be able to call methods with the `onlyApprovedContracts` modifier, but that is not the case. Fix this by ensuring every allowed address is a contract address by adding a check that the codesize in the address is > 0 when setting it in `setAllowedContracts`.
