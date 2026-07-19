---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md
tags:
- firm:zokyo
- report:2021-06-14-impossible-finance
title: Error in fee calculation.
vuln_class: []
---

# Error in fee calculation.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

ImpossibleLibrary.sol, Line 112
amountInPostFee = amountInPostFee.sub(sqrtK.sub(reserveIn));
- amountInPostFee is powered by 10000
- sqrtK.sub(reserveIn) - regular.
There is a calculation mistake with the loose of accuracy

**Recommendation**:

Fix the calculation mistake
