---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: Non-Standard ERC20 tokens could be locked in the contract
vuln_class: []
---

# Non-Standard ERC20 tokens could be locked in the contract

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

The ERC20 transfer function is used to transfer `rewardToken` tokens. However, some ERC20 tokens, such as USDT, BNB, and OMG, do not return a boolean. This can cause the `require(success, "Token transfer failed")` check to always fail, potentially resulting in tokens being locked in the contract.

**Recommendation**: 

To ensure compatibility with all ERC20 tokens and to handle transfer failures properly, it is recommended to use the SafeERC20 library from OpenZeppelin. This library provides a safe transfer function that properly handles tokens that do not return a value.

**Replace**:

```solidity
bool success = IERC20(rewardToken).transfer(owner(), amount);
```
With:
```solidity
SafeERC20.safeTransfer(IERC20(rewardToken), owner(), amount);
```
