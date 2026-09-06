---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Unused internal constants
vuln_class: []
---

# Unused internal constants

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

Constants STATUS_DEFAULT and STATUS_CANCELED declared in Burn.sol are never used in
Burn.sol

**Recommendation**: 

review the functionality or remove constants.
