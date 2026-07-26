---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: '`EmergencyVault::activateRecovery` can be DoS by a reverting `TARGET_VAULT`
  calls'
vuln_class: []
---

# `EmergencyVault::activateRecovery` can be DoS by a reverting `TARGET_VAULT` calls

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** `EmergencyVault::activateRecovery` does external calls to the `TARGET_VAULT` through `_harvestFees()` (which in turn calls `totalAssets()` then `_getProtocolBalance()`) and `_getProtocolBalance()` directly. `_getProtocolBalance()` performs external view calls to `TARGET_VAULT.balanceOf(address(this))` and `TARGET_VAULT.convertToAssets(...)`, which can revert if the target vault is compromised/upgradeable/misbehaving. As a result the recovery activation path can be DoSed by a reverting target vault, even when the adapter already holds recoverable assets locally.

**Impact:** In an incident where `TARGET_VAULT` becomes untrusted and its view functions revert, the vault may be unable activate `recoveryMode`. This can lock any assets already recovered to the vault contract, since users cannot redeem under the recovery flow until `recoveryMode` is set.

**Recommended Mitigation:** Refactor `activateRecovery()` to avoid relying on external target vault calls that can revert in incident scenarios. Remove `_getProtocolBalance()` from `activateRecovery()` (it’s only for event info) and let the fee harvesting be done manually after calls to `emergencyWithdraw` (if the `emergencyMode` restriction is removed or limited to only `EMERGENCY_ROLE`). Alternatively, add `_harvestFees()` at the end of `emergencyWithdraw()`.

**Lido:** Fixed in commit [`ee29862`](https://github.com/lidofinance/defi-interface/commit/ee298626d62e4d18f44b10a5cd6cbcbd3cae7188)

**Cyfrin:** Verified. `_harvestFees()` moved to `emergencyWithdraw()` and a `try/catch` added around the call to `_getProtocolBalance`.
