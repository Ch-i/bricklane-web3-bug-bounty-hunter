---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Borrowers immediately liquidated once Repayment resumes
vuln_class: []
---

# Borrowers immediately liquidated once Repayment resumes

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**

Given that liquidation is also paused along with repayment, if repayment is paused, during the pause the borrowers can become subject to liquidation due to market fluctuations. Now when repayment and liquidation are resumed simultaneously, borrowers will be liquidated immediately by liquidation bots unless they can front-run the bots transactions.

This will lead to borrowers being liquidated due to no fault of their own. 

**Recommendation**: 

It is advised to add a grace period after repayment resumes during which they can not be liquidated.

**Client commented**: 

We will inform users through our documents that users should always keep their position healthy either by depositing more collateral or repaying debt. Even if repay pauses, the borrower can keep health factor healthy by depositing.
