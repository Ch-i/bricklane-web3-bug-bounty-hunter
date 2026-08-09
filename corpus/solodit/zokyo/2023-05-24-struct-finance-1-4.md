---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Misleading value assignment to poolId
vuln_class: []
---

# Misleading value assignment to poolId

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

In contract TraderJoeYieldSource, according to the line: 175 in the constructor,
        poolId = isFarmExists ? _poolId : 0;

The poolId to _poolId in case the Farm exists. But it is entirely possible that the poolId is set to 0 even when the Farm exists by passing the _poolId parameter as 0 in the constructor. This would be contradictory to the fact that the poolId is set to 0 when the isFarmExists is false (i.e. the Farm does not exist) according to line: 175. 

**Recommendation**: 

It is advised to disallow passing _poolId as 0 in the constructor parameter to avoid unintended issues and logical flaws. 

**Comments**: 

The client said that the YieldSource contracts will be deployed manually by the struct team and that they will be validating the parameters before deployment
