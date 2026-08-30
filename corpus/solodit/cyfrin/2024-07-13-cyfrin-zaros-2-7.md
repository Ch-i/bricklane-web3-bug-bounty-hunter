---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Traders can't limit slippage and expiration time when creating market orders
vuln_class: []
---

# Traders can't limit slippage and expiration time when creating market orders

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Traders can't limit slippage and expiration time when creating market orders.

**Impact:** Traders' orders may be filled later and at a less favorable price than they were expecting.

**Recommended Mitigation:** Allow traders to specify the maximum slippage (acceptable price) they are willing to accept and the expiration time by which the order must be filled.

The price should be verified against the "Mark Price" which is stored in `ctx.fillPrice` in `SettlementBranch::_fillOrder`.

Interestingly in `leaves/MarketOrder.sol` the `Data` struct has a `timestamp` variable which is the timestamp when the trader created their order, but this is never checked when the order is filled.

**Zaros:** In commit [62c0e61](https://github.com/zaros-labs/zaros-core/commit/62c0e613ab02435dc0c3de9abdb14d7d880f2941) we have implemented a new "Off-Chain" order feature which allows users to specify a `targetPrice`. This feature is flexible enough to implement limit, stop, tp/sl and other types of trigger-based orders using some additional off-chain code.

**Cyfrin:** Verified that this new feature does provide a way for users to enforce slippage via the `targetPrice` condition. The new feature doesn't provide a deadline check but that is less important as presumably users are watching the status of the order and can cancel it off-chain. Also note that the security of this new feature has not been evaluated during this audit but will be evaluated in the competitive audit to follow.
