---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-03-27-global-interlink-0-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-03-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md
tags:
- firm:zokyo
- report:2023-03-27-global-interlink
title: Incorrect balance check
vuln_class: []
---

# Incorrect balance check

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2023-03-27-Global Interlink.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

In contract utility.move, in function `merge_and_split` at line 31 there’s an assertion between the base coin value and amount parameter. This is meant to ensure that there are enough remaining funds in the base coin balance, however there can be a case when the base coin remaining balance is equal to the amount parameter, so the assertion fails. This should not happen if the two values are equal.

**Recommendation**: 

Change the assertion from greater than to greater than or equal
