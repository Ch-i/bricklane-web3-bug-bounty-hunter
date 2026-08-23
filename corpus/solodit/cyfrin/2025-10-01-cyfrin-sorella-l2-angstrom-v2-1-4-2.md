---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-4-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: '`AngstromL2::beforeInitialize` conditionals can be combined'
vuln_class: []
---

# `AngstromL2::beforeInitialize` conditionals can be combined

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `AngstromL2::beforeInitialize` validates support for both dynamic fees and native currency within the pool key:

```solidity
function beforeInitialize(address, PoolKey calldata key, uint160)
    external
    view
    returns (bytes4)
{
    _onlyUniV4();
    if (key.currency0.toId() != NATIVE_CURRENCY_ID) revert IncompatiblePoolConfiguration();
    if (!LPFeeLibrary.isDynamicFee(key.fee)) revert IncompatiblePoolConfiguration();
    return this.beforeInitialize.selector;
}
```

These conditionals both revert with the same `IncompatiblePoolConfiguration()` custom error and so can be combined to save gas.

**Recommended Mitigation:**
```diff
function beforeInitialize(address, PoolKey calldata key, uint160)
    external
    view
    returns (bytes4)
{
    _onlyUniV4();
-   if (key.currency0.toId() != NATIVE_CURRENCY_ID) revert IncompatiblePoolConfiguration();
-   if (!LPFeeLibrary.isDynamicFee(key.fee)) revert IncompatiblePoolConfiguration();
+   if (key.currency0.toId() != NATIVE_CURRENCY_ID || !LPFeeLibrary.isDynamicFee(key.fee)) {
+       revert IncompatiblePoolConfiguration();
+   }
    return this.beforeInitialize.selector;
}
```

**Sorella Labs:** Acknowledged, will keep as is. Also no gas improvement was demonstrated, either way you're doing 2 branches because `||` does lazy evaluation and solc doesn't know how to optimize.

**Cyfrin:** Acknowledged.
