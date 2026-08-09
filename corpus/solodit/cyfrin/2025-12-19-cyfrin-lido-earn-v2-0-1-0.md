---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: Use named mappings to explicitly denote the purpose of keys and values
vuln_class: []
---

# Use named mappings to explicitly denote the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** Use named mappings to explicitly denote the purpose of keys and values:
```solidity
RewardDistributor.sol
52:    mapping(address => bool) private recipientExists;
```

**Lido:** Fixed in commit [4898c26](https://github.com/lidofinance/defi-interface/commit/4898c26cd0abc8426ad9e2220a8d7cac487ab9b8).

**Cyfrin:** Verified.
