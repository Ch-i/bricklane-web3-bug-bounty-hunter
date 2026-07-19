---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: '`call()` should be used instead of `transfer()` on address payable'
vuln_class: []
---

# `call()` should be used instead of `transfer()` on address payable

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** The `transfer()` and `send()` functions forward a fixed amount of 2300 gas. Historically, it has often been recommended to use these functions for value transfers to guard against reentrancy attacks. However, the gas cost of EVM instructions may change significantly during hard forks which may break already deployed contract systems that make fixed assumptions about gas costs. For example. EIP 1884 broke several existing smart contracts due to a cost increase of the `SLOAD` instruction. It is now therefore [no longer recommended](https://swcregistry.io/docs/SWC-134) to use these functions on address payable.

There are currently a [number](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L442) of [instances](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L642) where [use](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L646) of `transfer()` should be resolved.

**Impact:** The use of the deprecated `transfer()` function will cause transactions to fail:

* If `owner` calling `LimitOrderRegistry::withdrawNative`/`sender` calling `LimitOrderRegistry::claimOrder` is a smart contract that does not implement a payable function.
* If `owner` calling `LimitOrderRegistry::withdrawNative`/`sender` calling `LimitOrderRegistry::claimOrder` is a smart contract that does implement a payable fallback which uses more than 2300 gas unit.
* If `sender` calling `LimitOrderRegistry::claimOrder` is a smart contract that implements a payable fallback function that needs less than 2300 gas units but is called through proxy, raising the call's gas usage above 2300.
* Additionally, using higher than 2300 gas might be mandatory for some multi-signature wallets.

**Recommended Mitigation:** Use `call()` or solmate's `safeTransferETH` instead of `transfer()`, but be sure to respect the [Checks Effects Interactions (CEI) pattern](https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html).

**GFX Labs:** Fixed by using solmate `safeTransferETH` in commit [6c486c9](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/6c486c92598fda3582087d2ecd36f12238115eb1).

**Cyfrin:** Acknowledged.
