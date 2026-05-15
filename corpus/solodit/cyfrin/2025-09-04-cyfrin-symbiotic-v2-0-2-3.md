---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: Unused functions in `KeyRegistry`
vuln_class: []
---

# Unused functions in `KeyRegistry`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** In the `KeyRegistry` contract, there are three internal methods designed to handle 64-byte key operations:

* `_setKey64(address operator, uint8 tag, bytes memory key)`

* `_getKey64At(address operator, uint8 tag, uint48 timestamp)`

* `_getKey64(address operator, uint8 tag)`

However, none of these functions are ever invoked in the current contract implementation.

**Recommended Mitigation:** Remove the unused methods (`_setKey64`, `_getKey64`, `_getKey64At`) to improve code clarity, reduce audit surface area, and eliminate potential dead code.

**Symbiotic:** Acknowledged. Intended for future customizations.

**Cyfrin:** Acknowledged.
