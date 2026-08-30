---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-04-30-sophiaverse-ai-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-30-SophiaVerse.ai.md
tags:
- firm:zokyo
- report:2024-04-30-sophiaverse-ai
title: The `ModuleCanceled` event emits the wrong value for the timer parameter.
vuln_class: []
---

# The `ModuleCanceled` event emits the wrong value for the timer parameter.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-04-30-SophiaVerse.ai.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-30-SophiaVerse.ai.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

`ModuleCanceled` event emits the timer value of the module to be canceled for the third
parameter.
`densityModule_timer[_densityModule][_moduleId]` is emitted in the event but it is set to 0
before emitting.
So the `ModuleCanceled` event will always emit 0 for the timer parameter.

**Recommendation**:

Add a local variable for `densityModule_timer[_densityModule][_moduleId]` and emit the local
variable instead of `densityModule_timer[_densityModule][_moduleId]`.
