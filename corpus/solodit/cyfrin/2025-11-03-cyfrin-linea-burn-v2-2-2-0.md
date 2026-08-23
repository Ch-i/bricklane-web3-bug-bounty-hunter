---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Unnecessary ETH to WETH conversion during swap
vuln_class: []
---

# Unnecessary ETH to WETH conversion during swap

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** In the V3DexSwap contract, ETH is converted to WETH before processing the swap through the router as seen in the snippet below.

```solidity
IWETH9(WETH_TOKEN).deposit{ value: msg.value }();
IWETH9(WETH_TOKEN).approve(ROUTER, msg.value);
```

However, this is not required since the router supports direct ETH to Linea swaps. As we can observe below, the exactInputSingle function is marked as payable to allow direct ETH transfers when the function is called. In the router's execution path when the uniswapV3SwapCallback() calls the pay() function, it would process the router's contract balance if the token is WETH.

```solidity
File: SwapRouter.sol

/// @inheritdoc ISwapRouter
    function exactInputSingle(
        ExactInputSingleParams calldata params
    ) external payable override checkDeadline(params.deadline) returns (uint256 amountOut) {


File: PeripheryPayments.sol

/// @param token The token to pay
    /// @param payer The entity that must pay
    /// @param recipient The entity that will receive payment
    /// @param value The amount to pay
    function pay(
        address token,
        address payer,
        address recipient,
        uint256 value
    ) internal {
        if (token == WETH9 && address(this).balance >= value) {
            // pay with WETH9
            IWETH9(WETH9).deposit{value: value}(); // wrap only what is needed to pay
            IWETH9(WETH9).transfer(recipient, value);
        } else if (payer == address(this)) {
            // pay with tokens already in the contract (for the exact input multihop case)
            TransferHelper.safeTransfer(token, recipient, value);
        } else {
            // pull payment
            TransferHelper.safeTransferFrom(token, payer, recipient, value);
        }
    }
```

**Impact:** This does not pose a risk, however, it will cost unnecessary gas during swaps.

**Proof of Concept:** **Recommended Mitigation:**
Consider using ETH directly during swaps instead of converting to WETH.

**Linea:** Fixed at commit [a0b875](https://github.com/Consensys/linea-monorepo/pull/1620/commits/a0b875154412d5f543ad44994ca464219957b30e) and [dab9ebfd](https://github.com/Consensys/linea-monorepo/pull/1604/commits/dab9ebfdf65be8fbfecb9e2bc79d62056a60218b#diff-f36dd3901bbfa7a03d4cb920bfd8350752560a511fd7daf4a4fad33c7bbe6105)

**Cyfrin:** Verified. Now there are two versions of the DexSwap, one to directly swap ETH for Linea, and another to swap WETH for Linea. Both have been validated.
