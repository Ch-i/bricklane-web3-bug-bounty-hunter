---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Storage variables only assigned once in the constructor can be declared immutable
vuln_class: []
---

# Storage variables only assigned once in the constructor can be declared immutable

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** Storage variables which are only assigned once in the constructor can be declared immutable:

File: `StrategyFactory.sol`
```solidity
address public keeper;
```

File: `BeefyVaultConcLiqFactory.sol`
```solidity
BeefyVaultConcLiq public instance;
```

**Beefy:**
Acknowledged.
