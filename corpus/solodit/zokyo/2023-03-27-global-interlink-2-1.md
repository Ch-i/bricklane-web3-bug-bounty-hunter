---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-03-27-global-interlink-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-03-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md
tags:
- firm:zokyo
- report:2023-03-27-global-interlink
title: Insufficient sanity check for add_to_whitelist
vuln_class: []
---

# Insufficient sanity check for add_to_whitelist

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-03-27-Global Interlink.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In contract token_vesting.move, in function `add_to_whitelist` there are no sanity checks for the whitelist_address and whitelist_amount vectors, there is one check that is making sure the vectors have the same length, however both of the vectors could have length 0 which will break the function invariant as this function will execute successful but the store will not be modified in any way.

**Recommendation**: 

Add sanity checks to make sure that the arrays are not empty..
