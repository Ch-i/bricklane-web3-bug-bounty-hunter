---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[C-01] Anyone can move `EURS` tokens that the user allowed `FlorinTreasury`
  to spend'
vuln_class: []
---

# [C-01] Anyone can move `EURS` tokens that the user allowed `FlorinTreasury` to spend

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
High, as funds will be moved from a user's wallet unwillingly

**Likelihood:**
High, as it requires no preconditions and is a common attack vector

**Description**

The `depositEUR` method in `FlorinTreasury` looks like this:

```solidity
function depositEUR(address from, uint256 eurTokens) external whenNotPaused {
    eurTokens = Util.convertDecimals(eurTokens, 18, Util.getERC20Decimals(eurToken));
    SafeERC20Upgradeable.safeTransferFrom(florinToken, from, address(this), eurTokens);
    emit DepositEUR(_msgSender(), from, eurTokens);
}
```

The problem is that the `from` argument is user controlled, so anyone can check who has allowed the `FlorinTreasury` contract to spend his tokens and then pass that address as the `from` argument of the method. This will move `eurTokens` amount of `EURS` tokens from the exploited user to the `FlorinTreasury` contract, even though the user did not do this himself. The `depositEUR` method is expected to be called by `LoanVault::repayLoan` or `LoanVault::depositRewards`, where the user should first approve the `FlorinTreasury` contract to spend his `EURS` tokens. This is especially problematic if the user set `type(uint256).max` as the allowance of the contract, because in such case all of his `EURS` balance can be drained.

**Recommendations**

Use `msg.sender` instead of a user-supplied `from` argument, so tokens can only be moved from the caller's account.
