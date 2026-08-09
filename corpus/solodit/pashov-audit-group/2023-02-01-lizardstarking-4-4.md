---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-05] Filename and interface name mismatch'
vuln_class: []
---

# [I-05] Filename and interface name mismatch

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

In both `IEthLizards` and `IGenesisEthLizards` there is a mismatch between the filenames and the interface names - while the filenames write `Lizards` with a capital `L`, the interfaces use a lower-case one. Same problem is present for the `IUSDc` interface that is contained in the `IUSDC` file. Make sure to be consistent in the naming as this can lead to subtle errors.
