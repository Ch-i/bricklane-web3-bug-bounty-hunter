---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-20-cyfrin-myriad-realitio-oracle-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-20-cyfrin-myriad-realitio-oracle-v2-0
title: Pre-finalization return value `(0, false)` collides with `Outcomes.YES`
vuln_class: []
---

# Pre-finalization return value `(0, false)` collides with `Outcomes.YES`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md)_

---

**Description:** `getResult` returns `(0, false)` when the Reality.eth question has not yet been finalised:

```solidity
if (!realitio.isFinalized(questionId)) {
    return (0, false);
}
```

The integer `0` is numerically identical to `Outcomes.YES` (defined as `uint256 internal constant YES = 0` in `Outcomes.sol`). Any integration that reads the `outcome` return value without first checking `resolved == true` will silently interpret a pending, unresolved market as "resolved YES".

While correct callers should always guard on `resolved`, this is a latent footgun. The `IMarketOracle` interface provides no explicit sentinel to distinguish "not yet resolved" from "resolved YES", making defensive coding harder than necessary.

**Recommended Mitigation:** Return a value that cannot be confused with any valid resolved outcome when the market is unresolved.

```solidity
if (!realitio.isFinalized(questionId)) {
-   return (0, false);
+   return (-2, false);
}
```

**Myriad:** Fixed in commit [`fc2276a`](https://github.com/Polkamarkets/polkamarkets-js/commit/fc2276abd525ec99043ce1cff242f55e23ac775c)

**Cyfrin:** Verified.
