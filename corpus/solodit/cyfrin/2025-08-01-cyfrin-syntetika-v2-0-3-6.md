---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Remove obsolete `return` statements when using named return variables
vuln_class: []
---

# Remove obsolete `return` statements when using named return variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Remove obsolete `return` statements when using named return variables:
* `StakingVault::_withdrawTo, redeemTo`

**Syntetika:**
Fixed in commit [bd4bb12](https://github.com/SyntetikaLabs/monorepo/commit/bd4bb1222c2112bd33d02757872831d7f713dcdc).

**Cyfrin:** Verified.
