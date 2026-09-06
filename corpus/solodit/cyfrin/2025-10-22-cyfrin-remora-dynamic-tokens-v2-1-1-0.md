---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Pending payouts when resolving an investor are lost because there is no mechanism
  to claim the resolved payment
vuln_class: []
---

# Pending payouts when resolving an investor are lost because there is no mechanism to claim the resolved payment

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** When resolving a user who loses access to their account, the `ChildToken::resolveUser` function migrates balances, locks, and frozen tokens to a new address, ensuring the investor retains their previous balances. Even the pending payouts are calculated and assigned to the new address with the intention of allowing the investor to claim those pending payouts from the new account.

The problem is that no function allows an account to claim the calculated `resolvedPay`, which means the pending payouts for the old addresses are indeed migrated to the new addresses; however, the contracts don't offer a mechanism for investors to claim such payouts.
```solidity
///DividendManager.sol//
    function _resolvePay(address oldAddress, address newAddress) internal {
//@audit-issue => no function allows the `newAddress` to claim the payout of the `oldAddress` saved on the `_resolvedPay` mapping associated to the `newAddress`
@>      _getHolderManagementStorage()._resolvedPay[newAddress] = SafeCast.toUint128(_claimPayout(oldAddress));
        emit PaymentResolved(oldAddress, newAddress);
    }
```

Additionally, it is theoretically possible that payouts for an old address are lost if the newAddress is an address with an existing `resolvedPay` balance. The `DividendManager::_resolvePay` function assigns the calculated payout of the old address, regardless of whether the `resolvedPay` mapping has any value in it.

**Impact:** Pending payments for investors who lost access to their accounts and had their balances transferred to a new account via the `ChildToken::resolveUser` are lost.

**Recommended Mitigation:** Consider implementing a function that allows the new addresses to claim the calculated `resolvedPay` of the old addresses.

**Remora:** Fixed at commit [1a69894](https://github.com/remora-projects/remora-dynamic-tokens/commit/1a698942c15a8a0ab7b866bca2a6409bcb221828).

**Cyfrin:** Verified. Payouts of resolved users are claimable by the `newAddress` via the `ChildToken::claimPayout`
