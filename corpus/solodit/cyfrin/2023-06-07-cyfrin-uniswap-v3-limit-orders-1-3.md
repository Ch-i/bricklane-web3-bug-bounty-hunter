---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-1-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Fee-on-transfer/deflationary tokens will not be supported
vuln_class: []
---

# Fee-on-transfer/deflationary tokens will not be supported

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** When creating a new order, `LimitOrderRegistry::newOrder` assumes that the amount of deposited tokens is equal to the
function parameter plus the balance before the deposit. For tokens which take a fee on every transfer, this assumption does not hold and so the true amount transferred is less than the specified amount. As a result, tight slippage parameters in `_mintPosition` and `_addToPosition` which are calculated using this value will likely cause transactions to revert:
```solidity
uint128 amount0Min = amount0 == 0 ? 0 : (amount0 * 0.9999e18) / 1e18;
```
Additionally, the amount stored in `batchIdToUserDepositAmount` will be larger than the true balance deposited by a given user, resulting in incorrect accounting.

**Impact:** It will not be possible to use fee-on-transfer/deflationary tokens within the protocol.

**Recommended Mitigation:** Avoid allowlisting such problematic tokens. If it is desired to support such tokens then it recommended to cache token balances before and after any transfers, using the difference between those two balances rather than the input amount as the amount received.

**GFX Labs:** Acknowledged. This contract will not use fee-on-transfer or deflationary tokens.

**Cyfrin:** Acknowledged.
