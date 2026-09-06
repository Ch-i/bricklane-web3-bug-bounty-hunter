---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-0-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Lack of slippage protection in liquidity functions
vuln_class: []
---

# Lack of slippage protection in liquidity functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The `addLiquidity` and `removeLiquidity` functions do not include any form of slippage protection, such as `minSharesOut` or `minTokensOut` parameters. This means users cannot guard against receiving significantly fewer shares or tokens than expected due to changes in pool state between quoting and execution.

**Impact:** Without slippage bounds, users are exposed to unfavorable outcomes if the price shifts between the time they calculate expected results off-chain and when the transaction is executed. While this risk is mitigated on chains without public mempools (as currently targeted by the protocol), it becomes relevant on other EVM chains with public transaction visibility, where MEV actors or frontrunners may exploit such gaps.

**Proof of Concept:** Add the following test to `PredictionMarket.t.sol`:
```solidity
   function testFrontRunAddLiquidity() public {
        uint256 marketId = _createTestMarket();

        address alice = makeAddr("Alice");
        address bob = makeAddr("Bob");
        deal(address(tokenERC20), alice, 1 ether);
        deal(address(tokenERC20), bob, 1 ether);

        // bob sees that alice will add liquidity and buys shares to manipulate the price
        vm.startPrank(bob);
        tokenERC20.approve(address(predictionMarket), type(uint256).max);
        predictionMarket.buy(marketId, 1, 0, 10e16);
        vm.stopPrank();

        // alice adds liquidity
        vm.startPrank(alice);
        tokenERC20.approve(address(predictionMarket), type(uint256).max);
        predictionMarket.addLiquidity(marketId, 1e16);
        vm.stopPrank();

        // bob can now sell for more gaining ~30% of Alice deposit
        vm.prank(bob);
        predictionMarket.sell(marketId, 1, 10.3e16, type(uint256).max);
    }
```

**Recommended Mitigation:** Consider adding optional slippage parameters to both `addLiquidity` and `removeLiquidity`, e.g.:

```solidity
function addLiquidity(uint256 marketId, uint256 amount, uint256 minSharesOut) external;
function removeLiquidity(uint256 marketId, uint256 shares, uint256 minTokensOut) external;
```

These guardrails would allow users to constrain execution based on expected outcomes and improve safety if the protocol expands to other chains.

**Myriad:** Fixed in [PR#88](https://github.com/Polkamarkets/polkamarkets-js/pull/88), commit [`37e9e89`](https://github.com/Polkamarkets/polkamarkets-js/pull/88/commits/37e9e8912b6a8aee670bcc0002609df099cd7685)

**Cyfrin:** Verified. `addLiquidity` now takes a `minSharesIn` parameter and `removeLiquidity` takes a `minValue` parameter.
