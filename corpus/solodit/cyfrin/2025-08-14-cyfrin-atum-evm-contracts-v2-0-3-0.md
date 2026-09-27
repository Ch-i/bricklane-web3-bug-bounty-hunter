---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-3-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
Escrow.sol
66:        for (uint256 i = 0; i < allowlistedTokens.length; i++) {
270:        for (uint256 i = 0; i < length; i++) {
```

**Atum:**
Fixed in commit [6726871](https://github.com/Atum-Labs/evm-contracts/commit/672687134c9a65cba4c9eb1528c499e80bc80a49).

**Cyfrin:** Verified.

\clearpage
