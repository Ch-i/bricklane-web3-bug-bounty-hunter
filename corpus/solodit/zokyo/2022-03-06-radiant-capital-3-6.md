---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Commented code.
vuln_class: []
---

# Commented code.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MultiFee Distribution.sol: _withdraw Expired LocksFor(), line 1155. 
LiquidityZap.sol: standardAdd(), line 189; _addLiquidity(), lines 235-236. 
StargateBorrow.sol: setDAOTreasury(), line 94. 
Pre-production smart-contract should not contain commented code as it might mean that part of the contract's logic is unfinished. 

**Recommendation**: 

Remove or uncomment commented code.
