---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-3-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[L-01] Disallow aggregator withdrawals once the buyer side is confirmed'
vuln_class: []
---

# [L-01] Disallow aggregator withdrawals once the buyer side is confirmed

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [BuyerAggregator.sol](https://github.com/EthSign/tokentable-sellnow-swap-evm/blob/eafe0d070b48a51e65394fc7b6f4eb3928f9af12/src/BuyerAggregator.sol)

**Description:**

The `BuyerAggregator` allows buyers to withdraw their deposits at any time. However, this feature can introduce issues and cause the `SellNow` confirmation process to revert if buyers withdraw their funds after the aggregator has confirmed the buy side, but before the seller has confirmed their side of the process.

Once the aggregator confirms the buyer side, withdrawals should be disallowed to preserve the integrity of the session. However, if the seller cancels or fails to confirm before a defined deadline, buyers should regain the ability to withdraw their deposits.

**Impact:** Buyers may withdraw funds after confirmation, potentially breaking the `SellNow` confirmation flow and leading to denial of the confirmation process.

**Recommendation(s):** Consider restricting buyer withdrawals after buy-side confirmation, while also handling the scenario where the seller fails to confirm within the expected timeframe.

**Status:** Fixed

**Update from TokenTable:** [0aa773198e15addcdd9d42637ccc596020e28d46](https://github.com/EthSign/tokentable-sellnow-swap-evm/pull/11/commits/0aa773198e15addcdd9d42637ccc596020e28d46)
