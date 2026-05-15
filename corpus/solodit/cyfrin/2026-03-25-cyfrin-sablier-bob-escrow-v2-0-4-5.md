---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Add validation in `SablierBob::createOrder` to disallow same address as `buyer`
  and `seller`
vuln_class: []
---

# Add validation in `SablierBob::createOrder` to disallow same address as `buyer` and `seller`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Function `SablierBob::createOrder` does not check and disallow the `buyer` from being `msg.sender` (the seller) itself.

```solidity
function createOrder(
        IERC20 sellToken,
        uint128 sellAmount,
        IERC20 buyToken,
        uint128 minBuyAmount,
        address buyer,
        uint40 expiryTime
    )
```

**Recommended Mitigation:** Add validation to disallow the buyer and seller to be the same. Also consider preventing `sellToken == buyToken`.

**Sablier:** Acknowledged; adding the check would increase gas a bit for a typical use case. Even if buyer and seller are same, or buy and sell token are same, it does not introduce any risk or a concern. That’s why we decided to not take any action.
