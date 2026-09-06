---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: Address-based token identity checks can be bypassed by alias tokens and native
  ERC20 mirrors
vuln_class: []
---

# Address-based token identity checks can be bypassed by alias tokens and native ERC20 mirrors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** The protocol treats token identity as address equality (`tokenA == tokenB` and `tokenB == weth`). This assumption breaks when one economic asset has [multiple valid addresses (proxy aliases/wrapper aliases)](https://github.com/d-xo/weird-erc20?tab=readme-ov-file#multiple-token-addresses) or when [a chain exposes the native gas token as an ERC20](https://github.com/d-xo/weird-erc20?tab=readme-ov-file#erc-20-representation-of-native-currency).

**Impact:** Informational. Enabling orders that are "same asset, different address".

**Proof of Concept:** In `createOrder`, only `if (tokenA == tokenB) revert SameToken();` is enforced. In `createOrderWithEth`, only `if (tokenB == weth) revert SameToken();` is enforced. Both checks are address-only, so alias contracts for the same underlying asset can bypass these guards.

```solidity
audit-2026-02-ethcf-swapboard/contracts/src/Swapboard.sol
57:     function createOrder(
58:         address tokenA,
59:         uint256 amountA,
60:         address tokenB,
61:         uint256 amountB
62:     ) external nonReentrant returns (uint256 orderId) {
63:         if (tokenA == address(0)) revert ZeroAddress();
64:         if (tokenB == address(0)) revert ZeroAddress();
65:         if (amountA == 0) revert ZeroAmount();
66:         if (amountB == 0) revert ZeroAmount();
67:  >>>    if (tokenA == tokenB) revert SameToken();
68:         if (tokenA.code.length == 0) revert NotAContract(tokenA);
69:         if (tokenB.code.length == 0) revert NotAContract(tokenB);

--------- skipped -------

99:         emit OrderCreated(orderId, msg.sender, tokenA, amountA, tokenB, amountB);
100:     }


150:     function createOrderWithEth(
151:         address tokenB,
152:         uint256 amountB
153:     ) external payable nonReentrant returns (uint256 orderId) {
154:         if (msg.value == 0) revert ZeroETH();
155:         if (tokenB == address(0)) revert ZeroAddress();
156:         if (amountB == 0) revert ZeroAmount();
157:  >>>    if (tokenB == weth) revert SameToken();
158:         if (tokenB.code.length == 0) revert NotAContract(tokenB);

----- skipped -----

176:         emit OrderCreated(orderId, msg.sender, weth, msg.value, tokenB, amountB);
177:     }

```

**Recommended Mitigation:** No mitigation needed becasue of no impact. Just documentation / info.



**ETHCF:** Acknowledged; by design.
