---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Unused storage variable
vuln_class: []
---

# Unused storage variable

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

BaseContract.sol, _ReentrantCheck
Vault.sol, _ReentrantCheck
Variables are not used in the code.

**Recommendation**: 

Remove unused variables.
