---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-01-26-graviton-zero-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-01-26T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-01-26-Graviton%20Zero.md
tags:
- firm:zokyo
- report:2022-01-26-graviton-zero
title: View function will never return value.
vuln_class: []
---

# View function will never return value.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-01-26-Graviton Zero.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-01-26-Graviton%20Zero.md)_

---

**Description**


StakingB.sol Line 46
“stakesInfo” will never return value because it creates an array [from; to) but tries to iterate
through [from; to].

**Recommendation**:

Change the format of array to
“ s = new Stake[](_to - _from+1)” or
“for (uint256 i = _from; i < _to; i++)”
