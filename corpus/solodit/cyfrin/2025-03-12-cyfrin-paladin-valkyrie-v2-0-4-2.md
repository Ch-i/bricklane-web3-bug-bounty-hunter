---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-4-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Insufficient validation on the pool key in liquidity-modifying functions
vuln_class: []
---

# Insufficient validation on the pool key in liquidity-modifying functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** `FullRangeHook::addLiquidity` and `FullRangeHook::removeLiquidity` should only be callable with pools created via the hook itself; however there is a lack of validation on the pool key that means this is not strictly enforced. Instead, the current logic relies on the revert behavior when `IncentivizedERC20` functions are called on `address(0)` liquidity token.

**Recommended Mitigation:** The following validation should be added to explicitly enforce this requirement:

```diff
++ if (poolInfo[poolId].liquidityToken == address(0)) revert InvalidLiquidityToken();
```

**Paladin:** Fixed by commit [`5eef1b0`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/5eef1b068bf7d221794c7744ed32745b587bd771).

**Cyfrin:** Verified. Additional validation has been added.
