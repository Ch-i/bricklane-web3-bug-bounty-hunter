---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-12
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20RegistryService` storage-gap comment has the wrong slot count'
vuln_class: []
---

# `Tip20RegistryService` storage-gap comment has the wrong slot count

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** The storage comment says the contract declares 9 slots, but its own enumeration covers slots 0 through 9. The 10 declared slots plus the 40-slot gap still preserve the intended 50-slot window, so the implementation is correct.

**Recommended Mitigation:** Change the comment from 9 declared slots to 10.

**Securitize:** Fixed in [PR 14](https://github.com/securitize-io/bc-tempo-sc/pull/14).

**Cyfrin:** Verified.
