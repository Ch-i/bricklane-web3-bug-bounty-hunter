---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Using `calldata` is more efficient to `memory` for read-only external function
  inputs
vuln_class: []
---

# Using `calldata` is more efficient to `memory` for read-only external function inputs

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Using `calldata` is more efficient to `memory` for read-only external function inputs:

`PreDepositVault`:
```solidity
35:        , string memory name
36:        , string memory symbol
```

**Strata Money:**
"initialize" (__init_Vault) is now internal, so the calldata can't be used with the parameters.

**Cyfrin:** Acknowledged.
