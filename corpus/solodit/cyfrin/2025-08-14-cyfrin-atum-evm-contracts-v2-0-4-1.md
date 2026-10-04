---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-4-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Use constants for repeated identical hashes
vuln_class: []
---

# Use constants for repeated identical hashes

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** Use constants for repeated identical hashes:
* `Escrow::reserve` - cache `keccak256(abi.encodePacked(RESERVE_WITNESS_TYPE_STRING))` into `bytes32` constant `0x01bb854522a8c95ca13074640aa260f6131c081d2a4164e25221bba9be783d64`
* `Escrow::release` - cache `keccak256(abi.encodePacked(RELEASE_WITNESS_TYPE_STRING))` into `bytes32` constant `0xb212eeab69b3c25930c9e48c98f613ad8ea39b1ec0ebb1a75211a058de0b262b`
* `Escrow::refund` - cache `keccak256(abi.encodePacked(REFUND_WITNESS_TYPE_STRING))` into `bytes32` constant `0x6e3d08c38893b1ecbc6f42fbb57bb90bd2c29f9ebfbd95477768bfe4d7b85b7d`

**Atum:**
Fixed in commit [d304a6f](https://github.com/Atum-Labs/evm-contracts/commit/d304a6f5ac9ca282e7686a2396bfb789a11c343b).

**Cyfrin:** Verified.
