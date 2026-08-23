---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Lack of Macro Attributes for Pausable Derivation
vuln_class: []
---

# Lack of Macro Attributes for Pausable Derivation

_Section severity (from Solodit section header): Low_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

For example, if users want to change the storage key of Pausable in examples/pausable-examples/pausable\_base/src/lib.rs line 7-12, he will add #[pausable(paused\_storage\_key="new\_storage\_key") However, the rust compiler cannot compile it due to the error.

**Recommendations:** 

Add attributes(pausable) to derive\_pausable.
