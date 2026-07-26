---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Events parameters not indexed
vuln_class: []
---

# Events parameters not indexed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract VaultETH_V2, none of the events has `indexed` parameters to ease out the filter of event logs. Indexing seller and buyer parameters in the Sell and Buy events, respectively, is advised.

**Recommendation**: 

Update the events to index the suggested parameters.
