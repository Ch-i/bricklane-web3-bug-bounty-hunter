---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`TradingAccount::deductAccountMargin` can incorrectly add the same values
  multiple times to output parameter `marginDeductedUsdX18`'
vuln_class: []
---

# `TradingAccount::deductAccountMargin` can incorrectly add the same values multiple times to output parameter `marginDeductedUsdX18`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** In `TradingAccount::deductAccountMargin`, `ctx.settlementFeeDeductedUsdX18`, `ctx.orderFeeDeductedUsdX18`, and `ctx.pnlDeductedUsdX18` are added to `marginDeductedUsdX18` inside the `for` loop:
```solidity
File: TradingAccount.sol
443:             marginDeductedUsdX18 = marginDeductedUsdX18.add(ctx.settlementFeeDeductedUsdX18);
458:             marginDeductedUsdX18 = marginDeductedUsdX18.add(ctx.orderFeeDeductedUsdX18);
475:             marginDeductedUsdX18 = marginDeductedUsdX18.add(ctx.pnlDeductedUsdX18);
```

**Impact:** As those 3 values are accumulated withdrawn collateral amounts, the same amount will be added several times and `marginDeductedUsdX18` will be larger than expected.

**Proof of Concept:** Consider a scenario where:
* the settlement fee `if` statement executes once with `ctx.isMissingMargin == false`
* this then increments `marginDeductedUsdX18` by `ctx.settlementFeeDeductedUsdX18`
* the order fee `if` statement executes once with `ctx.isMissingMargin == true`
* this triggers `continue` which immediately jumps to next loop iteration
* the settlement fee `if` statement is skipped since the settlement fee has been paid
* `marginDeductedUsdX18` is again incremented by `ctx.settlementFeeDeductedUsdX18` !

In this scenario `marginDeductedUsdX18` was incremented twice by `ctx.settlementFeeDeductedUsdX18`. The same thing can happen with `ctx.orderFeeDeductedUsdX18`.

**Recommended Mitigation:** Update `marginDeductedUsdX18` at the end of the function instead of inside the loop:

```solidity
function deductAccountMargin() {
    for (uint256 i = 0; i < globalConfiguration.collateralLiquidationPriority.length(); i++) {
        /* snip: loop processing */
        // @audit removed updates to `marginDeductedUsdX18` during loop
    }

    // @audit update `marginDeductedUsdX18` only once at end of loop
    marginDeductedUsdX18 = ctx.settlementFeeDeductedUsdX18.add(ctx.orderFeeDeductedUsdX18).add(ctx.pnlDeductedUsdX18);
}
```

**Zaros:** Fixed in commit [9bcf9f8](https://github.com/zaros-labs/zaros-core/commit/9bcf9f83d11d8da9113c38f01404985f37dc763d).

**Cyfrin:** Verified.
