---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-3-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[L-03] Use call(...) instead of transfer(...)'
vuln_class: []
---

# [L-03] Use call(...) instead of transfer(...)

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [BuyerAggregator.sol](https://github.com/EthSign/tokentable-sellnow-swap-evm/blob/eafe0d070b48a51e65394fc7b6f4eb3928f9af12/src/BuyerAggregator.sol#L152)

**Description:**

The `BuyerAggregator` allows users to withdraw their deposited funds via the `withdrawDeposit(...)` function. When native ETH is used as the payment token, the contract sends ETH during withdrawal using the low-level `transfer(...)` call. This method has a fixed gas limit, which may cause withdrawals to revert when interacting with smart wallets or contracts that require more gas to accept ETH.

It is generally recommended to use the low-level `call(...)` to avoid such reverting scenarios. However, `call(...)` introduces a reentrancy risk and must be handled with caution. Furthermore, if you introduce the `call(...)`, after execution it returns a boolean value indicating success of the call rather than reverting on failure.

**Impact:** Withdrawals may revert for users with smart contract wallets.

**Recommendation(s):** - Consider replacing `transfer(...)` with a low-level `call(...)`, and ensure the return value is checked for success.

If switching to `call(...)` is not preferred, consider adding an explicit `recipient` parameter to allow users to withdraw to an EOA, reducing the likelihood of failed transfers.

**Status:** Fixed

**Update from TokenTable:** [520ae0070e21837211885a4760636bfc6df53363](https://github.com/EthSign/tokentable-sellnow-swap-evm/pull/11/commits/520ae0070e21837211885a4760636bfc6df53363)
