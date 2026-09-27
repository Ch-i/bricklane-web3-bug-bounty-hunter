---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-4
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
title: '`Tip20TrustService::_setRole` emits abstract-role events after native calls'
vuln_class: []
---

# `Tip20TrustService::_setRole` emits abstract-role events after native calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20TrustService::_setRole` updates storage, performs native token and registry calls, and only then emits its abstract-role events. This differs from the documented event-before-external-call convention. Transaction reversion remains atomic, so contract state is not corrupted.

**Recommended Mitigation:** Either document the existing log order or emit the abstract-role change before native external calls, preserving checks-effects-interactions and relying on transaction reversion to remove logs on failure.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.
