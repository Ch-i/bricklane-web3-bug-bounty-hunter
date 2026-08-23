---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-01-sentiment-0x-aura-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-01-Sentiment-0x-Aura.md
tags:
- firm:zachobront
- report:2023-05-01-sentiment-0x-aura
title: '[L-02] If ETH is used as an input and output token to 0x, it will always revert'
vuln_class: []
---

# [L-02] If ETH is used as an input and output token to 0x, it will always revert

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-05-01-Sentiment-0x-Aura.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-01-Sentiment-0x-Aura.md)_

---

When transaction data to `transformERC20()` is decoded, the following check is made:
```solidity
(address tokenOut, address tokenIn) =
    abi.decode(data[4:], (address, address));

if (tokenIn == ETH) {
    tokensOut = new address[](1);
    tokensOut[0] = tokenOut;
    return (true, new address[](0), tokensOut);
}

if (tokenOut == ETH) {
    tokensIn = new address[](1);
    tokensIn[0] = tokenIn;
    return (true, tokensIn, new address[](0));
}
```
The intention is that, if a token going in or out of our sentiment wallet is ETH, we return an empty array. This is because (a) Sentiment balances automatically account for ETH and (b) the address representing ETH (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) is not a real token, so calls to it would revert.

However, in the case where both the `inputToken` and `outputToken` are ETH, the check above fails.

When the first `if` statement is triggered (because `tokenIn == ETH`), we assume the `outputToken` is not ETH and set `tokensOut[0] = tokenOut`.

Since `tokenOut` is ETH, this is returning a token with the value `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` to our account.

Tracing this back through Sentiment, the result is:
- we call `_updateTokensOut()` with `tokensOut` as `[0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE]`
- for each token in `tokensOut`, we call `tokensOut[i].balanceOf(account)`
- since `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` is not a real token, this call reverts

**Proof of Concept**

Here is a test that can be dropped into `0xTransform.t.sol` demonstrating this issue:

```solidity
function testEthOutIfAlsoIn() public {
    ITransformERC20Feature.Transformation[] memory transformations = new ITransformERC20Feature.Transformation[](0);
    bytes memory data = abi.encodeWithSelector(
        ITransformERC20Feature.transformERC20.selector, ETH, ETH, 0, 0, transformations
    );

    (bool canCall, address[] memory tokensIn, address[] memory tokensOut) =
        controllerFacade.canCall(target, true, data);

    assert(tokensOut[0] == ETH);
}
```

**Recommendation**

Add a nested check to the first `if` statements to ensure this situation is accounted for:
```diff
if (tokenIn == ETH) {
+   if (tokenOut == ETH) return (true, new address[](0), new address[](0));
    tokensOut = new address[](1);
    tokensOut[0] = tokenOut;
    return (true, new address[](0), tokensOut);
}

// no need to check it here because it would already be caught above
if (tokenOut == ETH) {
    tokensIn = new address[](1);
    tokensIn[0] = tokenIn;
    return (true, tokensIn, new address[](0));
}
```

**Review**

Acknowledged. This situation seems unlikely to happen, and the Sentiment team has chosen not to address the issue.
