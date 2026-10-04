---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-17-cyfrin-atumv2-evm-tron-v2-0-0-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-10-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-17-cyfrin-atumv2-evm-tron-v2-0
title: Don't initialize to default values in Solidity
vuln_class: []
---

# Don't initialize to default values in Solidity

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md)_

---

**Description:** Don't initialize to default values in Solidity:
```solidity
FulfillmentProxy.sol
23:        for (uint256 i = 0; i < params.length; i++) {
```

**Atum:**
Fixed in commit [f899054](https://github.com/Atum-Labs/evm-contracts/commit/f899054ef1b970cac20ff068f5bda2b15aca3e69) for EVM and [ee83857](https://github.com/Atum-Labs/tvm-contracts/commit/ee83857255f982c019f996b3b5b8b08d6e733ada) for TRON.

**Cyfrin:** Verified.
