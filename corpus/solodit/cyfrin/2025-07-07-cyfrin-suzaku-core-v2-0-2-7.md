---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Hardcoded gas limit for hook in `onSlash` may cause reverts
vuln_class: []
---

# Hardcoded gas limit for hook in `onSlash` may cause reverts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `onSlash` function in the `BaseDelegator` contract conditionally invokes a hook via a low-level `call` if a hook address is set:

```solidity
assembly ("memory-safe") {
    pop(call(HOOK_GAS_LIMIT, hook_, 0, add(calldata_, 0x20), mload(calldata_), 0, 0))
}
```

This call uses a **hardcoded gas limit (`HOOK_GAS_LIMIT`)**, and the function enforces that at least `HOOK_RESERVE + HOOK_GAS_LIMIT * 64 / 63` gas is available before proceeding. If this requirement is not met, the function reverts with `BaseDelegator__InsufficientHookGas`.

This rigid gas enforcement introduces a fragility: if the hook's execution requires more gas than allocated by `HOOK_GAS_LIMIT`, the `call` may silently fail or the transaction may revert entirely.

**Impact:** Hooks that require more gas than the hardcoded limit will consistently fail, potentially breaking integrations.

As protocol complexity grows, hardcoded gas limits become brittle and may hinder composability or future extensions.

**Recommendation:**

Consider introducing a mechanism for the hook gas limit to be configured by the contract owner.

**Suzaku:**
Acknowledged.

**Cyfrin:** Acknowledged.
