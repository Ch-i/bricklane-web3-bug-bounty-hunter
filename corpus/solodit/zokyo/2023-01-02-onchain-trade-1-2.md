---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Lock solidity pragma
vuln_class: []
---

# Lock solidity pragma

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Low

**Status**: Unresolved

**Description**

Contracts should be deployed with the same compiler version and flags that they have been tested the most with. Lock the pragma to a specific version, since not all the compiler versions support all the features.

**Recommendation**: 

Lock pragma to version at least 0.8.12 to support all the features.

**Note #1**: Minor change has been made, but it did not fix/address the issue.
