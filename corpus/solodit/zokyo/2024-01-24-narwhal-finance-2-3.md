---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: No address(0) check
vuln_class: []
---

# No address(0) check

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract PythOracle.sol, the method rescueFunds() does not validate if _receiver is address(0) or not. If accidentally set to address(0), funds would be lost.

In Contract PairInfos.sol, the method initialize(...) transfers ownership to address _owner which is not validated to be address(0) or not.

In Contract Trading.sol, the method initialize(...) transfers ownership to address _owner which is not validated to be address(0) or not.

**Recommendation**: 

Add a check to validate if the given parameter is address(0) or not.
