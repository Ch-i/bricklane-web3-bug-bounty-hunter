---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-16-cyfrin-ethena-timelock-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-05-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-16-cyfrin-ethena-timelock-v2-0
title: Only emit events if state actually changes
vuln_class: []
---

# Only emit events if state actually changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-16-cyfrin-ethena-timelock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md)_

---

**Description:** A number of functions in `EthenaTimelockController` will emit events even if the state did not change since they simply write to storage but don't read the current storage value to check if it is changing.

Ideally these functions would revert or at least not emit events if the state did not change:
* `addToWhitelist`
* `removeFromWhitelist`

**Ethena:** Acknowledged.

\clearpage
