---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-19-the-forevver-association-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-11-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-The%20Forevver%20Association.md
tags:
- firm:zokyo
- report:2024-11-19-the-forevver-association
title: Unused Constants in Fias Token Contract
vuln_class: []
---

# Unused Constants in Fias Token Contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-11-19-The Forevver Association.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-The%20Forevver%20Association.md)_

---

**Severity** - Informational

**Status** - Acknowledged

**Description**:

The Fias token contract defines two constants, GLOBAL_LIMIT and CONTRACT_ADMIN, which are not utilized within the contract's implementation. The GLOBAL_LIMIT is set to 350,000,000, presumably intended to represent the maximum total supply of tokens. The CONTRACT_ADMIN is defined as an address, likely meant for administrative functions. However, neither of these constants is referenced in any of the contract's functions or logic.


**Recommendation**:


If these constants are intended for future use:
Document their intended purpose in comments above each constant.
Implement the functionality that utilizes these constants, such as enforcing the global token limit or adding admin-only functions.
If these constants are no longer needed:
Remove the unused constants to improve code clarity and slightly reduce deployment gas costs.
For the GLOBAL_LIMIT:
If it's meant to represent the maximum token supply, consider implementing a check in the initialize function to ensure the total minted amount doesn't exceed this limit.
For the CONTRACT_ADMIN:
If administrative functions are planned, implement them with appropriate access control using this address.
Consider using OpenZeppelin's Ownable or AccessControl contracts for more robust admin functionality.

**Client comment**: no impact, the admin functions that previously used those constants were removed and they only remain for clarity/readability.
