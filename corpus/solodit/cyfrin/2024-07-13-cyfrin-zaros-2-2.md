---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Remove max open interest check when liquidating in `LiquidationBranch::liquidateAccounts`
vuln_class: []
---

# Remove max open interest check when liquidating in `LiquidationBranch::liquidateAccounts`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** In `LiquidationBranch::liquidateAccounts` there is no point calling `PerpMarket::checkOpenInterestLimits` since:
* the liquidation will always be decreasing the open interest so the liquidation can't cause the max open interest limit to be breached
* the skew check is not performed

Hence there is no need for this check when liquidating. The danger of having this check is that if the admin sets the max open interest limit below the current open interest then all liquidations will revert.

**Recommended Mitigation:**
```diff
- (ctx.newOpenInterestX18, ctx.newSkewX18) = perpMarket.checkOpenInterestLimits(
-     ctx.liquidationSizeX18, ctx.oldPositionSizeX18, sd59x18(0), false
- );
```

**Zaros:** Fixed in commit [783ea67](https://github.com/zaros-labs/zaros-core/commit/783ea67979b79bce3a74dbaf19e53503034c9349).

**Cyfrin:** Verified.
