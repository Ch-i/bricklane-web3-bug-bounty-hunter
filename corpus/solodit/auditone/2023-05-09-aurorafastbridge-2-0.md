---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: Missing comparison between lock\_time\_min and lock\_time\_max in set\_lock\_time
  function
vuln_class: []
---

# Missing comparison between lock\_time\_min and lock\_time\_max in set\_lock\_time function

_Section severity (from Solodit section header): Low_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:**

In the set\_lock\_time function, the lock\_time\_min and lock\_time\_max values are not compared before setting the lock\_duration. This might lead to a situation where lock\_time\_min is greater than lock\_time\_max, which could be an invalid state for the intended logic of the application.

**Recommendation:** 

To prevent potential issues with invalid lock duration configurations, we recommend adding a comparison between lock\_time\_min and lock\_time\_max before updating the lock\_duration. If lock\_time\_min is greater than lock\_time\_max, the function should return an error or panic to indicate that the provided values are invalid.
