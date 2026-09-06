---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-03-27-global-interlink-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-03-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md
tags:
- firm:zokyo
- report:2023-03-27-global-interlink
title: Constant defined by a value that has not yet been published in the documentation
vuln_class: []
---

# Constant defined by a value that has not yet been published in the documentation

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-03-27-Global Interlink.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In contract utility.move the const EPOCH_SECONDS is supposed to be the time duration of an epoch in seconds. This const will affect the value returned by the functions `get_current_timestamp` and `get_timestamp_from_now_by_days`. The time duration of an epoch is present in the documentation just as an example, and there is no certainty that the value will remain the same.

**Recommendation**: 

Be aware that the value of the const EPOCH_SECONDS comes from an example and not from the official documentation and there is no certainty that the value will remain the same and update the code accordingly.
