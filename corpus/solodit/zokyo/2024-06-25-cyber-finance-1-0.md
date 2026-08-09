---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: Centralization Risk due to overpowered owner
vuln_class: []
---

# Centralization Risk due to overpowered owner

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**


The CyberFinance contract introduces a significant centralization risk due to its reliance on the owner for critical functions, including pausing/unpausing the contract, increasing/decreasing claimable balances, and withdrawing tokens. This centralized control can lead to potential abuse or single points of failure, particularly if the owner account is compromised or if the owner acts maliciously.

**Recommendation**: 

To mitigate centralization risks, consider implementing multisig wallets or time-locked functions for critical operations.

**Comment**: 

The client stated that the project is planned to set up a multisig for the owner wallet to mitigate the centralization.
