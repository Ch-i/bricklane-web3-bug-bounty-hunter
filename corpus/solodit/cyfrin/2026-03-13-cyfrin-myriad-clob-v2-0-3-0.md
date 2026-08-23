---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-0
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
title: Orders have no maximum fee protection
vuln_class: []
---

# Orders have no maximum fee protection

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** The `Order` struct does not include a `maxFeeBps` field. Fee rates are looked up from `FeeModule` at settlement time by the operator. If a fee admin updates fees between when a user signs an order and when the operator settles it, the user has no protection against unexpectedly high fees. The operator controls the timing of settlement and can observe fee changes before executing matches.

```solidity
struct Order {
    address trader;
    uint256 marketId;
    uint8 outcomeId;
    Side side;
    uint256 amount;
    uint256 price;
    uint256 minFillAmount;
    uint256 nonce;
    uint256 expiration;
    // No maxFeeBps field
};
```

While this can be exploited from a malicious operator, this will still negatively affect users when the operator acts in good faith. For example increasing the fee rate to increase protocol revenue will result in existing orders paying an unexpected cost that they did not agree to.

**Impact:** Users sign orders with an expectation of current fee rates, but have no on-chain guarantee. A fee admin could increase fees to 100% BPS (10000), and the operator could settle existing orders at those rates. While the operator is trusted, this represents an unnecessary trust assumption that can be eliminated with a simple order field.

**Recommended Mitigation:** Add a `maxFeeBps` field to the `Order` struct and validate during settlement:

```solidity
struct Order {
    // ... existing fields ...
    uint256 maxFeeBps; // maximum total fee the trader accepts
};

// In _matchOrders or settlement:
require(applicableFeeBps <= order.maxFeeBps, "fee exceeds max");
```

**Myriad:** We acknowledge this behaviour, however we'd like to point out that:

- Even though it's possible, changing market fees while trading is open is not a behaviour we'd expect to happen/execute in our end.
- In the rare event of triggering market fee updates mid-market, it would certainly be with the intent of lowering them, not raising them. And no ever fee increase would ever be made without warning users of the execution date, giving them enough time to cancel their open orders.
