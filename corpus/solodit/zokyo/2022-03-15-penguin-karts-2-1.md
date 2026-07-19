---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: Missed messages in exceptions
vuln_class: []
---

# Missed messages in exceptions

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

Token.sol. In case of discrepancy in requirements the error will not return a description of
exception. It will make it harder to reveal a cause of revert.

**Recommendation**:

Use messages in “require” statements to add a description of exceptions.
