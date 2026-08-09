---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: emiting `EthReceived` event when `RollupRevenueVault` receives 0 eth
vuln_class: []
---

# emiting `EthReceived` event when `RollupRevenueVault` receives 0 eth

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** [`RollupRevenueVault::receive`](https://github.com/Consensys/linea-monorepo/blob/8285efababe0689aec5f0a21a28212d9d22df22e/contracts/src/operational/RollupRevenueVault.sol#L292-L294) && [`RollupRevenueVault:fallback`](https://github.com/Consensys/linea-monorepo/blob/8285efababe0689aec5f0a21a28212d9d22df22e/contracts/src/operational/RollupRevenueVault.sol#L285-L287) functions emit the `EthReceived` event whenever they are called, regardless of whether there was actually any native sent to the contract.

Especially for the `fallback()`, the event will be emitted whenever the function catches a call that doesn't match any of the functions specified on the ABI.


**Recommended Mitigation:** Consider skipping the event emission when no native is received on the `fallback` or `receive` functions.

**Linea:** Fixed at [PR 1604](https://github.com/Consensys/linea-monorepo/pull/1604)

**Cyfrin:** Verified. Both `receive()` and `fallback()` functions revert if `msg.value` is 0.
