---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Possible Integer Overflow/Underflow in quicksort function in utils library
vuln_class: []
---

# Possible Integer Overflow/Underflow in quicksort function in utils library

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

The use of `uint(left + (right - left) / 2)` might result in an overflow if the right is a very large negative number. Consider validating the array indices to avoid potential overflow issues.
