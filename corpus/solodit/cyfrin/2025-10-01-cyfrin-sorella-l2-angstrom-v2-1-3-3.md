---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Modifier-style base `Ownable()` constructor call can be removed from `AngstromL2`
vuln_class: []
---

# Modifier-style base `Ownable()` constructor call can be removed from `AngstromL2`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `AngstromL2` inherits the `Ownable` contract which has no constructor. Instead, it is expected that the `_initializeOwner()` function is called, as is currently the case:

```solidity
constructor(IPoolManager uniV4, address owner, IFlashBlockNumber flashBlockNumberProvider)
    UniConsumer(uniV4)
@>  Ownable()
{
@>  _initializeOwner(owner);
    ...
}
```

Therefore, the modifier-style base constructor call without arguments can be removed to silent the `forge lint` error.

**Recommended Mitigation:**
```diff
constructor(IPoolManager uniV4, address owner, IFlashBlockNumber flashBlockNumberProvider)
    UniConsumer(uniV4)
-   Ownable()
{
    _initializeOwner(owner);
    ...
}
```

**Sorella Labs:** Acknowledged, prefer explicit constructor invocation.

**Cyfrin:** Acknowledged.
