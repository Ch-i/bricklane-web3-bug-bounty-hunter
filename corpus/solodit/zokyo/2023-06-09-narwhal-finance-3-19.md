---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-19
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: PRECISION storage variable can be constant
vuln_class: []
---

# PRECISION storage variable can be constant

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

In TradingStorage contract, PRECISION variable (line#13) has been updated to be not constant while making the contract upgradeable. 
Since there is no method to update the PRECISION value, PRECISION can be constant and it will be compatible with upgradeability as well. The same is mentioned in OpenZeppelin’s doc.

**Recommendation**: 

Update PRECISION variable to be constant. 

**Fixed**: Issue Acknowledged in commit a72e06b
