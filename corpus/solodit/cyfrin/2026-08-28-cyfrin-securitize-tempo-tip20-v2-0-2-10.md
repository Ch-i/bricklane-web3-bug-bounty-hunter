---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-10
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`ITip20TrustService` misdocuments `MASTER` native permissions'
vuln_class: []
---

# `ITip20TrustService` misdocuments `MASTER` native permissions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `ITip20TrustService` says `MASTER` receives no native grants. `Tip20TrustService::_project`, the README, and the protocol specification instead define `MASTER` as the union of all token and registry permissions. The implementation is correct; the published interface understates the strongest key's authority.

**Recommended Mitigation:** Update the interface role table and `setServiceOwner` documentation to list the complete `MASTER` projection. Leave `NONE` as the only role with no native grants.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.
