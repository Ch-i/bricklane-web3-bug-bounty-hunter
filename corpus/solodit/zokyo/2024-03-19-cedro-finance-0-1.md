---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Repay allows to deposit without any upper limit
vuln_class: []
---

# Repay allows to deposit without any upper limit

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

In Contract Branch.sol, the method repayRequest(...) allows any user to repay their loan amount. However, there is no check on the amount being repaid. 

In Contract Core.sol, the repay(..) has the logic to deposit any extra amount other than the repay amount and mint ceTokens for the user.
Any user can use this method to deposit and mint ceTokens for any amount without any upper limit even after the deposit cap has been reached.

**Recommendation**: Add a check on `repayRequest(...)` method to not allow deposit amount more than the deposit cap.
