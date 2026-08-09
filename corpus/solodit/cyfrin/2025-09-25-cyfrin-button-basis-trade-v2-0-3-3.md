---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Unused `Pocket::approve` function
vuln_class: []
---

# Unused `Pocket::approve` function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** The `Pocket` contract defines an `approve` function, but this function is never invoked within the current system architecture. Maintaining unused or unreferenced code increases the protocol’s attack surface, as the function may be misused in future upgrades, or create assumptions that are no longer valid.

**Recommended Mitigation:** If the approve function is not required, remove it entirely.

**Button:** Acknowledged. Will be used in a new contract.
