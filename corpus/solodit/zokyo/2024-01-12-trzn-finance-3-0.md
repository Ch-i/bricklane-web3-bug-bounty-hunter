---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Manipulate112 Should Manipulate To uint112 Instead Of 128
vuln_class: []
---

# Manipulate112 Should Manipulate To uint112 Instead Of 128

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**

The function manipulate112 manipulates a int128  whereas it should be applied to int112 instead 

**Recommendation**: 

Cast to a int112 instead
