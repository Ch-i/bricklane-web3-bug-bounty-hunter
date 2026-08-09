---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Outdated reference to urBEAN3CRV Convert
vuln_class: []
---

# Outdated reference to urBEAN3CRV Convert

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

There are multiple instances in `LibConvert::getMaxAmountIn` and `LibConvert::getAmountOut` that reference conversion to urBEAN3CRV and BEAN:3CRV. Since the underlying liquidity has now been migrated to the BEAN:ETH Well, it is no longer possible to convert Unripe Bean or Unripe LP to BEAN:3CRV. Therefore, the following diff should be applied:

```diff
function getMaxAmountIn(address tokenIn, address tokenOut)
    internal
    view
    returns (uint256)
{
    /// BEAN:3CRV LP -> BEAN
    if (tokenIn == C.CURVE_BEAN_METAPOOL && tokenOut == C.BEAN)
        return LibCurveConvert.lpToPeg(C.CURVE_BEAN_METAPOOL);

    /// BEAN -> BEAN:3CRV LP
    if (tokenIn == C.BEAN && tokenOut == C.CURVE_BEAN_METAPOOL)
        return LibCurveConvert.beansToPeg(C.CURVE_BEAN_METAPOOL);

    // Lambda -> Lambda
    if (tokenIn == tokenOut)
        return type(uint256).max;

    // Bean -> Well LP Token
    if (tokenIn == C.BEAN && tokenOut.isWell())
        return LibWellConvert.beansToPeg(tokenOut);

    // Well LP Token -> Bean
    if (tokenIn.isWell() && tokenOut == C.BEAN)
        return LibWellConvert.lpToPeg(tokenIn);

-   // urBEAN3CRV Convert
+   // urBEAN:ETH Convert
    if (tokenIn == C.UNRIPE_LP){
-       // urBEAN:3CRV -> urBEAN
+       // urBEAN:ETH -> urBEAN
        if(tokenOut == C.UNRIPE_BEAN)
            return LibUnripeConvert.lpToPeg();
-       // UrBEAN:3CRV -> BEAN:3CRV
+       // UrBEAN:ETH -> BEAN:ETH
-       if(tokenOut == C.CURVE_BEAN_METAPOOL)
+       if(tokenOut == C.BEAN_ETH_WELL)
        return type(uint256).max;
    }

    // urBEAN Convert
    if (tokenIn == C.UNRIPE_BEAN){
-       // urBEAN -> urBEAN:3CRV LP
+       // urBEAN -> urBEAN:ETH LP
        if(tokenOut == C.UNRIPE_LP)
            return LibUnripeConvert.beansToPeg();
        // UrBEAN -> BEAN
        if(tokenOut == C.BEAN)
            return type(uint256).max;
    }

    revert("Convert: Tokens not supported");
}

function getAmountOut(address tokenIn, address tokenOut, uint256 amountIn)
    internal
    view
    returns (uint256)
{
    /// BEAN:3CRV LP -> BEAN
    if (tokenIn == C.CURVE_BEAN_METAPOOL && tokenOut == C.BEAN)
        return LibCurveConvert.getBeanAmountOut(C.CURVE_BEAN_METAPOOL, amountIn);

    /// BEAN -> BEAN:3CRV LP
    if (tokenIn == C.BEAN && tokenOut == C.CURVE_BEAN_METAPOOL)
        return LibCurveConvert.getLPAmountOut(C.CURVE_BEAN_METAPOOL, amountIn);

-   /// urBEAN:3CRV LP -> urBEAN
+   /// urBEAN:ETH LP -> urBEAN
    if (tokenIn == C.UNRIPE_LP && tokenOut == C.UNRIPE_BEAN)
        return LibUnripeConvert.getBeanAmountOut(amountIn);

-   /// urBEAN -> urBEAN:3CRV LP
+   /// urBEAN -> urBEAN:ETH LP
    if (tokenIn == C.UNRIPE_BEAN && tokenOut == C.UNRIPE_LP)
        return LibUnripeConvert.getLPAmountOut(amountIn);

    // Lambda -> Lambda
    if (tokenIn == tokenOut)
        return amountIn;

    // Bean -> Well LP Token
    if (tokenIn == C.BEAN && tokenOut.isWell())
        return LibWellConvert.getLPAmountOut(tokenOut, amountIn);

    // Well LP Token -> Bean
    if (tokenIn.isWell() && tokenOut == C.BEAN)
        return LibWellConvert.getBeanAmountOut(tokenIn, amountIn);

    // UrBEAN -> Bean
    if (tokenIn == C.UNRIPE_BEAN && tokenOut == C.BEAN)
        return LibChopConvert.getConvertedUnderlyingOut(tokenIn, amountIn);

-   // UrBEAN:3CRV -> BEAN:3CRV
+   // UrBEAN:ETH -> BEAN:ETH
-   if (tokenIn == C.UNRIPE_LP && tokenOut == C.CURVE_BEAN_METAPOOL)
+   if (tokenIn == C.UNRIPE_LP && tokenOut == C.BEAN_ETH_WELL)
        return LibChopConvert.getConvertedUnderlyingOut(tokenIn, amountIn);

    revert("Convert: Tokens not supported");
}
```
