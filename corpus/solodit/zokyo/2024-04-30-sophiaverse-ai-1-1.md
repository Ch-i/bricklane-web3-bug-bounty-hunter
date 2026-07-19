---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-04-30-sophiaverse-ai-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-30-SophiaVerse.ai.md
tags:
- firm:zokyo
- report:2024-04-30-sophiaverse-ai
title: Unnecessary if condition for `densityModule_timer[_densityModule][_module]`.
vuln_class: []
---

# Unnecessary if condition for `densityModule_timer[_densityModule][_module]`.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-04-30-SophiaVerse.ai.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-30-SophiaVerse.ai.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

https://github.com/SentienceQuest/heirloom/blob/main/src/Heirloom.sol#L55
In the `moduleSupportedRequirements()` modifier, if `ownerOfWill` is not zero, there is no need
to check if `densityModule_timer[_densityModule][_module]` is zero because
`densityModule_owner` and `densityModule_timer` variables are set to non-zero or zero at the
same time.

**Recommendation**:

Remove if condition for `densityModule_timer`.
