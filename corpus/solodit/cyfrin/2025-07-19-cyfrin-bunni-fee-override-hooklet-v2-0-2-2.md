---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0
title: '`BeforeSwapFeeOverride` struct could be used in the `FeeOverride` struct'
vuln_class: []
---

# `BeforeSwapFeeOverride` struct could be used in the `FeeOverride` struct

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md)_

---

**Description:** The `BeforeSwapFeeOverride` and `BeforeSwapPriceOverride` structs defined in `IHooklet` are not currently used:

```solidity
/// @notice Overrides the swap fee of a pool before the swap is executed.
/// Ignored if the pool has an am-AMM manager.
/// @member overridden If true, the swap fee is overridden.
/// @member fee The swap fee to use for the swap. 6 decimals.
struct BeforeSwapFeeOverride {
    bool overridden;
    uint24 fee;
}

/// @notice Overrides the pool's spot price before the swap is executed.
/// @member overridden If true, the pool's spot price is overridden.
/// @member sqrtPriceX96 The spot price to use for the swap. Q96 value.
struct BeforeSwapPriceOverride {
    bool overridden;
    uint160 sqrtPriceX96;
}
```

The `FeeOverride` struct defined in `FeeOverrideHooklet` could instead be comprised of two `BeforeSwapFeeOverride` members for zero/one:

```solidity
struct FeeOverride {
    bool overrideZeroToOne;
    uint24 feeZeroToOne;
    bool overrideOneToZero;
    uint24 feeOneToZero;
}
```

**Recommended Mitigation:**
```diff
    struct FeeOverride {
-       bool overrideZeroToOne;
-       uint24 feeZeroToOne;
-       bool overrideOneToZero;
-       uint24 feeOneToZero;
+       BeforeSwapFeeOverride overrideZeroToOne;
+       BeforeSwapFeeOverride overrideOneToZero;
    }
```

**Bacon Labs:** Rather than use the struct definitions, we've decided to remove them from the core contracts
entirely in commit [fc18b04](https://github.com/Bunniapp/bunni-v2/pull/135/commits/fc18b0434c3fb487cc91f6c8dd3cc7b29549b137) as they were unused. As such, we will not be implementing the suggested fix.

**Cyfrin:** Acknowledged. The upstream unused structs have been removed
