---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Use a specific version of Solidity instead of a wide version
vuln_class: []
---

# Use a specific version of Solidity instead of a wide version

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StratFeeManagerInitializable` should use `pragma solidity 0.8.23;` instead of `pragma solidity ^0.8.23;`.

**Beefy:**
Acknowledged.
