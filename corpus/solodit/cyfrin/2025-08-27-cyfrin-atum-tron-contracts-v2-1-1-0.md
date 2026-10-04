---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-27-cyfrin-atum-tron-contracts-v2-1-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md
tags:
- firm:cyfrin
- report:2025-08-27-cyfrin-atum-tron-contracts-v2-1
title: '`Fulfillment::requestHash` should reference `depositId` generated inside `Escrow::deposit`'
vuln_class: []
---

# `Fulfillment::requestHash` should reference `depositId` generated inside `Escrow::deposit`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-27-cyfrin-atum-tron-contracts-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md)_

---

**Description:** Currently `Fulfillment::requestHash` (emitted in the `Fulfilled` event on the destination chain) references `DepositWitness::requestId`.

However this is not very useful and potentially dangerous when reconciling fulfillments to requests off-chain, since the input `DepositWitness::requestId`:
* is never stored anywhere on-chain
* may not be unique as it is an arbitrary input supplied by the `Originator`

**Recommended Mitigation:** The `Fulfilled` event should instead reference the `depositId` which is created inside `Escrow::deposit`, is always unique and is also stored on-chain.

**Atum:**
Fixed in commit [7049c6c](https://github.com/Atum-Labs/tvm-contracts/commit/7049c6cbd71c3e9b5984fa9e9da520869a09f732) for `tvm-contracts` and [3dc4563](https://github.com/Atum-Labs/evm-contracts/commit/3dc45631509cc39a8242484ecb53396c4d412293) for `evm-contracts`.

**Cyfrin:** Verified.
