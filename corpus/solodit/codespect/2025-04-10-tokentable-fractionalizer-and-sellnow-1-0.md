---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[H-01] Aggregator does not approve token spending'
vuln_class: []
---

# [H-01] Aggregator does not approve token spending

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [BuyerAggregator.sol](https://github.com/EthSign/tokentable-sellnow-swap-evm/blob/101eff63f094aafd9f5ea7bcd1025acba2e272f0/src/BuyerAggregator.sol#L86-L97)

**Description:**

The `BuyerAggregator` contract collects funds from whitelisted buyers (in ETH or an ERC20 token) to facilitate the purchase of future tokens, which are later fractionalized via the `ShareFractionalizer`. The deposit token is defined by the `SellNow` session configuration. Once the required amount is collected, the `confirm()` function is called to finalize the process. This performs two key actions:

1. Locks the aggregator from accepting further deposits;
2. Calls `sellNow.confirm()` to proceed with the buyer-side confirmation;

However, when the `sellNow.confirm()` function is later called from the seller side, it will revert because the aggregator does not approve the `SellNow` contract to transfer the payment tokens on its behalf.

Since ERC20 transfers initiated by external contracts require explicit approval, the lack of an `approve(...)` call prevents the funds from being moved to the seller, halting the process.

**Impact:** Denial of service: the selling process cannot be completed because the aggregator has not authorized the `SellNow` contract to transfer the required tokens. As a result, the seller cannot receive their funds, and the finalisation of the session remains stuck.

**Recommendation(s):** Add an `approve(...)` call for the payment token (including any associated fees) to the `SellNow` before calling `sellNow.confirm()`

**Status:** Fixed

**Update from TokenTable:** [1b00e2c2e3daf853d320440668a812e075889ee7](https://github.com/EthSign/tokentable-sellnow-swap-evm/pull/11/commits/1b00e2c2e3daf853d320440668a812e075889ee7)
