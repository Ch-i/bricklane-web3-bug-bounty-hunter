---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-04-30-sophiaverse-ai-1-2
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
title: The wrong spell in the `ModuleBenefiaryReplaced` event name.
vuln_class: []
---

# The wrong spell in the `ModuleBenefiaryReplaced` event name.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-04-30-SophiaVerse.ai.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-30-SophiaVerse.ai.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

https://github.com/SentienceQuest/heirloom/blob/main/src/Heirloom.sol#L25
`ModuleBenefiaryReplaced` should be replaced with `ModuleBeneficiaryReplaced`.

**Recommendation**:

Change the event name to `ModuleBeneficiaryReplaced`.
