---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: '`IBeforeInitializeHook` should be added to the `AngstromL2` inheritance chain'
vuln_class: []
---

# `IBeforeInitializeHook` should be added to the `AngstromL2` inheritance chain

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `AngstromL2.sol` imports the `IBeforeInitializeHook` interface; however, it is not currently used. Given that `AngstromL2` is expected to implement this hook, it should be added to the inheritance chain:

```diff
contract AngstromL2 is
    UniConsumer,
    Ownable,
+   IBeforeInitializeHook
    IBeforeSwapHook,
    IAfterSwapHook,
    IAfterAddLiquidityHook,
    IAfterRemoveLiquidityHook
{
    ...
}
```

**Sorella Labs:** Fixed in commit [724759d](https://github.com/SorellaLabs/l2-angstrom/commit/724759d9f673cda2b48565b00052bb541349cfa0).

**Cyfrin:** Verified.
