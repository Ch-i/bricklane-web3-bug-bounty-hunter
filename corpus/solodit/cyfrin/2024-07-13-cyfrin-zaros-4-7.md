---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Use input `amount` in `TradingAccountBranch::withdrawMargin` when calling `safeTransfer`
vuln_class: []
---

# Use input `amount` in `TradingAccountBranch::withdrawMargin` when calling `safeTransfer`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Remove redundant conversion by using input `amount` in `TradingAccountBranch::withdrawMargin` when [calling](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/branches/TradingAccountBranch.sol#L298-L300) `safeTransfer` at the end:

```diff
- uint256 tokenAmount = marginCollateralConfiguration.convertUd60x18ToTokenAmount(ud60x18Amount);
- IERC20(collateralType).safeTransfer(msg.sender, tokenAmount);
+IERC20(collateralType).safeTransfer(msg.sender, amount);
```

**Zaros:** Fixed in commit [a4d64ac](https://github.com/zaros-labs/zaros-core/commit/a4d64acf400561143b3e261037d6dd152b85c9a4).

**Cyfrin:** Verified.
