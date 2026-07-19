---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
RewardDistributor.sol
143:        uint256 totalBps = 0;
145:        for (uint256 i = 0; i < recipients_.length; i++) {
230:        for (uint256 i = 0; i < recipientsLength; i++) {
```

**Lido:** Fixed in commit [4898c26](https://github.com/lidofinance/defi-interface/commit/4898c26cd0abc8426ad9e2220a8d7cac487ab9b8) for `totalBps`.

**Cyfrin:** Verified.
