---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: Redundant Modifier Invocation in Withdraw Functions
vuln_class: []
---

# Redundant Modifier Invocation in Withdraw Functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

The `onlyOwner` modifier is invoked twice in `withdrawBalance` and `withdraw` functions, leading to inefficiency in the smart contract. Both functions perform a similar check that could be consolidated.

**Recommendation**: 

To improve the efficiency, refactor the withdraw logic into an internal function. Both `withdraw` and `withdrawBalance` can then call this internal function, ensuring that the modifiers are applied only once. This reduces redundancy and improves code readability and efficiency.
