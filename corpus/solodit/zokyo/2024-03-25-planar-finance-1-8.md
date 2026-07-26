---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Ensuring Secure Token Transfers in Smart Contracts with OpenZeppelin's SafeTransfer
vuln_class: []
---

# Ensuring Secure Token Transfers in Smart Contracts with OpenZeppelin's SafeTransfer

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Location**: Presale.sol, line 322, 324

**Description**:

The use of `.transfer()` for token transactions, while common, can pose significant security risks, particularly due to its inability to handle token transfer failures gracefully. This limitation becomes apparent in the context of ERC-20 tokens, where transfers might fail for various reasons, such as lack of allowance or insufficient balance. To mitigate these risks and ensure robust error handling, it's advisable to adopt OpenZeppelin's `safeTransfer` function from its ERC-20 library.

The provided `_safeClaimTransfer` function attempts to securely transfer `PROJECT_TOKENs` by checking the contract's balance and transferring the lesser of the desired amount or the available balance. However, it relies on the basic transfer method, which returns a boolean value to indicate success or failure. This approach requires explicit, manual checking of the transfer outcome, as demonstrated by the require statement to revert the transaction if `transferSuccess` is false.

**Recommendation:**

To enhance security and reliability, replace the basic transfer call with OpenZeppelin's safeTransfer method.
