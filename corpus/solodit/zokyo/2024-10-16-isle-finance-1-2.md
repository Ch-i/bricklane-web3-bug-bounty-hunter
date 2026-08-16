---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: 'Optimization: Redundant Checks in depositWithPermit Function'
vuln_class: []
---

# Optimization: Redundant Checks in depositWithPermit Function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Location**: Pool.sol

**Description**: 

The current implementation of the depositWithPermit function uses the deposit function, which performs redundant checks that depositWithPermit has already handled.
```solidity
66      shares_ = deposit(assets_, receiver_);
```
This inefficiency can be mitigated by using the previewDeposit function to calculate the share amount and then directly calling _deposit for the actual deposit.

**Recommendation**: 

Replace the line shares_ = deposit(assets_, receiver_); in the depositWithPermit function with:
```solidity
shares = previewDeposit(assets);
_deposit(_msgSender(), receiver, assets, shares);
```
This change eliminates redundant checks and improves the efficiency of the depositWithPermit function.

**Comment**: 

Client confirms to follow the recommendation to fix it.
