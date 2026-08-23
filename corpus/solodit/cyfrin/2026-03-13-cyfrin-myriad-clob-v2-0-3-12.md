---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-12
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Consider enforcing a minimum order amount
vuln_class: []
---

# Consider enforcing a minimum order amount

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `_validateOrder` only requires `order.amount > 0`:

```solidity
// MyriadCTFExchange.sol:398
require(order.amount > 0, "amount 0");
```

There is no lower bound on the fill size. Very small orders are technically valid and will be processed by the settlement engine, but they produce negligible or zero notional due to integer division (e.g. `(fillAmount * price) / ONE = 0` for tiny `fillAmount`), waste operator gas, and pollute the on-chain `filledAmounts` mapping with dust entries. The protocol does catch zero-notional fills via `require(notional > 0)` in some paths, but this is a reactive guard rather than a proactive size floor.

A related issue arises with partial fills: if an order for `amount = 1000` is partially filled to `995` and the minimum is `10`, the remaining `5` can never satisfy the minimum and the order is effectively stranded, the operator cannot legally fill the remainder and the trader must cancel to free the slot.

Enforcing minimum sizes off-chain in the operator is the most common approach and is likely already done, but an on-chain minimum provides defence in depth: it protects against operator misconfiguration, future integrations that bypass the off-chain layer, and ensures the invariant is auditable from the contract alone.

**Recommended Mitigation:** Add a configurable `minOrderAmount` to the exchange (settable by admin) and check it in `_validateOrder` and at the fill site:

```solidity
uint256 public minOrderAmount;

// in _validateOrder:
require(order.amount >= minOrderAmount, "below min amount");

// after updating filledAmounts in _matchOrders / matchCrossMarketOrders:
uint256 remaining = order.amount - filledAmounts[orderHash];
require(remaining == 0 || remaining >= minOrderAmount, "dust remainder");
```

The dust-remainder check ensures every partial fill either completes the order or leaves a fillable amount. This can equivalently be enforced off-chain by the operator before submitting a fill.

**Myriad:** **Cyfrin:**
