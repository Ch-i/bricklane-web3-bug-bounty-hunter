---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-07-21-itrustfinance-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2021-07-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md
tags:
- firm:zokyo
- report:2021-07-21-itrustfinance
title: Gas optimization by omitting extra variable
vuln_class: []
---

# Gas optimization by omitting extra variable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-07-21-ITrustFinance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md)_

---

**Description**

It is possible to call a method immediately without writing to a variable.
![image](https://github.com/user-attachments/assets/1ae826d4-9a58-497f-8033-edb855a2d9af)

**Recommendation**:

Call the method immediately without writing to a variable.
