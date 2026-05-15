---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Potential Security Risk in using `emergencyWithdrawFunds` Function
vuln_class: []
---

# Potential Security Risk in using `emergencyWithdrawFunds` Function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Informational

**Status**:  Unresolved

**Description**:

The `emergencyWithdrawFunds` function present in most contracts of the project allows the contract owner to withdraw funds (both ETH and ERC20 tokens) to their address. While this function includes an `onlyOwner` modifier ensuring that only the contract owner can call it, there is a potential risk of misuse leading to a rug pull scenario if not properly safeguarded.

**Recommendations**:

- Implement a multi-signature requirement for calling this function.
- Introduce a time lock or delay mechanism to provide transparency before funds are withdrawn.
- Clearly document the conditions under which this function can be used and communicate them to the community.
