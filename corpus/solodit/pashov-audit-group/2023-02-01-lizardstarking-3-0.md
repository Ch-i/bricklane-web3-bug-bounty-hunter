---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[L-01] Functionality from docs is missing'
vuln_class: []
---

# [L-01] Functionality from docs is missing

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The Gitbook says: `In order to claim rewards, the user will also need to engage in at least one on-chain governance vote/action with their Ethlizards, to ensure active participation. `. This functionality is not present in the contract and can lead to false assumptions from users/protocol devs. Either remove it from the docs or update the code by implementing it.
