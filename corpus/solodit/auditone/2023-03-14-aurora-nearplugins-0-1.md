---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Mismatched Variable Names
vuln_class: []
---

# Mismatched Variable Names

_Section severity (from Solodit section header): High_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

if users want to add except() arguments on function decrease\_1in examples/pausable-examples/pausable\_base/src/lib.rs line 49-52. However, the rust compiler cannot compile it due to the error:

**Recommendations:**

In the function get\_bypass\_condition, we use variable \_\_check\_paused. But in function if\_paused we use variable check\_paused.They should be the same variable. Change the variable check\_paused to \_\_check\_paused in function if\_paused
