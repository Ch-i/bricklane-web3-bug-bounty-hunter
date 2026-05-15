---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Don't initialize to default values
vuln_class: []
---

# Don't initialize to default values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Don't initialize to default values as Solidity already does this:
```solidity
predeposit/MetaVault.sol
220:        for (uint i = 0; i < length; i++) {
241:        for (uint i = 0; i < assetsArr.length; i++) {
```

**Strata:** Fixed in commit [07b471f](https://github.com/Strata-Money/contracts/commit/07b471f8292d62098ee4ffd97e62d6f0854d96ce).

**Cyfrin:** Verified.
