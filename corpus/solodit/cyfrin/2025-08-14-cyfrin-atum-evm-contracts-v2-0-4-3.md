---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-4-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Cache identical storage reads
vuln_class: []
---

# Cache identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** Cache identical storage reads:
* `Escrow.sol`
```solidity
// cache `depositInfo.settler` before `require` check
183:        require(depositInfo.settler != address(0), Escrow_SettlerNotSet(witness.depositId));
190:        address settler = depositInfo.settler;
```

**Atum:**
Fixed in commit [6726871](https://github.com/Atum-Labs/evm-contracts/commit/672687134c9a65cba4c9eb1528c499e80bc80a49).

**Cyfrin:** Verified.
