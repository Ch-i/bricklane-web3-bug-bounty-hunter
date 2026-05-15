---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Use `calldata` instead of `memory` for function arguments that do not get mutated
vuln_class: []
---

# Use `calldata` instead of `memory` for function arguments that do not get mutated

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** Use `calldata` instead of `memory` for function arguments that do not get mutated:

File:BeefyVaultConcLiq.sol
```solidity
47:        string memory _name,
48:        string memory _symbol
```

**Beefy:**
Fixed in commit [8349866](https://github.com/beefyfinance/experiments/commit/8349866c048412ec4c395eb0666b9e5aad6d6447).

**Cyfrin:** Verified.

\clearpage
