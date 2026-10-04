---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-1-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[H-03] Native ETH is not supported by SellNow contract'
vuln_class: []
---

# [H-03] Native ETH is not supported by SellNow contract

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [SellNow.sol](https://github.com/EthSign/tokentable-sellnow-swap-evm/blob/101eff63f094aafd9f5ea7bcd1025acba2e272f0/src/SellNow.sol)

**Description:**

The `BuyerAggregator` contract collects funds from whitelisted buyers (in ETH or an ERC20 token) to facilitate the purchase of future tokens, which are later fractionalized via the `ShareFractionalizer`. The type of token accepted is defined in the `SellNow` session configuration. Once the required amount is collected, the `confirm()` function is called to finalize the process. This function:

1. Locks the aggregator from accepting further deposits;
2. Calls `sellNow.confirm()` to proceed with the buyer-side confirmation;

As previously mentioned, the aggregator supports native ETH deposits. However, the `SellNow` contract is not capable of receiving ETH during the `confirm(...)` call. Moreover, due to the two-step confirmation process, it is not feasible to use `transferFrom` with native ETH—this method only works for ERC20 tokens.

This results in a fundamental incompatibility between ETH-based sessions and the payment mechanism in `SellNow`.

Furthermore, it is currently not possible to establish a session using native ETH as the payment token. In the aggregator, native ETH is represented as `address(0)`, but this configuration is not properly handled during session creation and results in an invalid setup.

**Impact:** Denial of service: ETH collected by the aggregator cannot be used to pay and finalize the session in the `SellNow` contract. As a result, the confirmation process fails, and the sale cannot be completed.

**Recommendation(s):** Introduce special handling for ETH payments. Two possible solutions:

- Wrap ETH into WETH within the aggregator before confirming, allowing compatibility with ERC20 logic;
- Define a separate ETH-specific execution path for `SellNow.confirm()` that accepts native ETH;

**Status:** Fixed

**Update from TokenTable:** [423c967dc3596720bb92bd258ad55007263dc888](https://github.com/EthSign/tokentable-sellnow-swap-evm/pull/11/commits/423c967dc3596720bb92bd258ad55007263dc888)

**Update from CODESPECT:** The issue has been resolved. The TokenTable team has chosen to wrap the ETH to WETH. In case the seller does not confirm their part of the escrow process, an owner-only function `withdrawDepositOwner(...)` was introduced to allow withdrawal of these tokens.

This function also updates the payment token, which introduces a level of centralisation. However, this trade-off was accepted to prevent scenarios where ETH from deposits could remain stuck in the contract due to wrapping complications.
