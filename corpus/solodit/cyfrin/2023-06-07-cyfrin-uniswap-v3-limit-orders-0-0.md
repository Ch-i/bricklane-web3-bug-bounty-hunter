---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Calls to `LimitOrderRegistry::newOrder` might revert due to overflow
vuln_class: []
---

# Calls to `LimitOrderRegistry::newOrder` might revert due to overflow

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** Reasonable input could cause an arithmetic overflow when opening new orders because large multiplications are performed on variables defined as `uint128` instead of `uint256`. Specifically, in `LimitOrderRegistry::_mintPosition` and `LimitOrderRegistry::_addToPosition` the following lines (which appear in both functions) are problematic:

```solidity
uint128 amount0Min = amount0 == 0 ? 0 : (amount0 * 0.9999e18) / 1e18;
uint128 amount1Min = amount1 == 0 ? 0 : (amount1 * 0.9999e18) / 1e18;
```

**Impact:** It is not possible for users to create new orders with deposit amounts in excess of `341e18`, limiting the protocol to working with comparatively small orders.

**Proof of Concept:** Paste this test into `test/LimitOrderRegistry.t.sol`:

```solidity
function test_OverflowingNewOrder() public {
    uint96 amount = 340_316_398_560_794_542_918;
    address msgSender = 0xE0b906ae06BfB1b54fad61E222b2E324D51e1da6;
    deal(address(USDC), msgSender, amount);
    vm.startPrank(msgSender);
    USDC.approve(address(registry), amount);

    registry.newOrder(USDC_WETH_05_POOL, 204900, amount, true, 0);
}
```

**Recommended Mitigation:** Cast the `uint128` value to `uint256` prior to performing the multiplication:

```solidity
uint128 amount0Min = amount0 == 0 ? 0 : uint128((uint256(amount0) * 0.9999e18) / 1e18);
uint128 amount1Min = amount1 == 0 ? 0 : uint128((uint256(amount1) * 0.9999e18) / 1e18);
```

**GFX Labs:** Fixed by changing multipliers from 18 decimals to 4 decimals in commits [f9934fe](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/f9934fe5d5eaaf061f4dab110a7b99efda7efb20) and [c731cd4](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/c731cd4d579af3aebd7a75c00bc9aa4ddb45f112).

**Cyfrin:** Acknowledged.
