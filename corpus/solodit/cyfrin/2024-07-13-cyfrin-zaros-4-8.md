---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Remove redundant `unary` call from `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd`
vuln_class: []
---

# Remove redundant `unary` call from `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd` [L239](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/leaves/TradingAccount.sol#L239) does this:
```solidity
UD60x18 markPrice = perpMarket.getMarkPrice(unary(sd59x18(position.size)), perpMarket.getIndexPrice());
```

The `unary` [function](https://github.com/PaulRBerg/prb-math/blob/main/src/sd59x18/Helpers.sol#L88-L90) takes as input a `SD59x18`, unwraps it, applies `-` to change sign then re-wraps it. Hence there is no point wrapping `position.size` first; simply apply `-` on the native type then wrap it.

**Recommended Mitigation:** Use this more efficient and simpler version:
```solidity
UD60x18 markPrice = perpMarket.getMarkPrice(sd59x18(-position.size), perpMarket.getIndexPrice());
```

The same change could also be made in `LiquidationBranch::liquidateAccounts`, eg:
```diff
ctx.oldPositionSizeX18 = sd59x18(position.size);
- ctx.liquidationSizeX18 = unary(ctx.oldPositionSizeX18);
+ ctx.liquidationSizeX18 = sd59x18(-position.size);
```

**Zaros:** Fixed in commit [5ffe8f4](https://github.com/zaros-labs/zaros-core/commit/5ffe8f4a1e07a322f3d1ce9da6ec885dd7d69c3c).

**Cyfrin:** Verified.
