---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Parallel governor value in IsleGlobal and Receivable contract may result in
  two separate governor addresses
vuln_class: []
---

# Parallel governor value in IsleGlobal and Receivable contract may result in two separate governor addresses

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Location**: IsleGlobal.sol,Receivable.sol

**Description**: 

The governor address for the Isle protocol has the authority to make changes and modify settings which are critical to the protocol’s day to day operations. This address is stored in both the Receivable and IsleGlobal contract however, since the address is set twice (once for each contract), this may cause inconsistent addresses resulting in inconsistent data if one were to be changed but not the other due to human error or some other reason. 

**Recommendation**

It’s recommended that the Governable inherited contract is removed from the Receivable contract and the governor address is obtained from IsleGlobal.
