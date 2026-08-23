---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Change public functions to external where possible to save gas
vuln_class: []
---

# Change public functions to external where possible to save gas

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In contract Flashloan.sol, at line 18 function flashLoan is declared as public but never used for internal calls, no reason to be public.

**Recommendation**: 

Change function from public to external
