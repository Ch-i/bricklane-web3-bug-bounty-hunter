---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`backing_memory.cpp` preprocessor guard inconsistent with header'
vuln_class: []
---

# `backing_memory.cpp` preprocessor guard inconsistent with header

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`backing_memory.cpp:20`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/backing_memory.cpp#L20) and [`backing_memory.hpp:36`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/backing_memory.hpp#L36), the preprocessor guards for file-backed storage features differ:

| File | Guard |
|------|-------|
| `backing_memory.hpp:36` | `#if !defined(__wasm__) && !defined(_WIN32)` |
| `backing_memory.cpp:20` | `#if !defined(__wasm__) \|\| defined(ENABLE_WASM_BENCH)` |

Two inconsistencies:

1. **Missing `_WIN32` exclusion in `.cpp`** — The header excludes Windows, but the `.cpp` doesn't. On Windows the `.cpp` defines symbols (`storage_budget`, `current_storage_usage`, `parse_size_string`) that nothing can reference because the header never declares them.

2. **`ENABLE_WASM_BENCH` not recognized by header** — The `.cpp` allows WASM builds when `ENABLE_WASM_BENCH` is defined, but the header has no such exception. When building with both `__wasm__` and `ENABLE_WASM_BENCH`, the `.cpp` provides definitions that are invisible to any translation unit including the header.

In UltraHonk production (Linux/macOS), file-backed storage is only activated when `BB_SLOW_LOW_MEMORY=1` is set. Windows and WASM are not supported production targets.

**Impact:** Informational. No impact on production prover or verifier.

**Recommended Mitigation:** Make [`backing_memory.cpp:20`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/backing_memory.cpp#L20) match [`backing_memory.hpp:36`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/backing_memory.hpp#L36):

```diff
-#if !defined(__wasm__) || defined(ENABLE_WASM_BENCH)
+#if !defined(__wasm__) && !defined(_WIN32)
```

**Aztec:**
Acknowledged.
