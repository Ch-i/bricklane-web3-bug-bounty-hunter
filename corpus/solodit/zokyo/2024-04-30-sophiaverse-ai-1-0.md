---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-04-30-sophiaverse-ai-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-30-SophiaVerse.ai.md
tags:
- firm:zokyo
- report:2024-04-30-sophiaverse-ai
title: could be set immutable.
vuln_class: []
---

# could be set immutable.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-04-30-SophiaVerse.ai.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-30-SophiaVerse.ai.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

`densityModule0`, `densityModule1`, `densityModule2`, `densityModule3`, `densityModule4`
variables are only set in the constructor.

**Recommendation**:

Set the variables immutable.
