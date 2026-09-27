---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-15
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
title: '`Tip20RegistryService::initialize` does not reject a zero `admin`'
vuln_class: []
---

# `Tip20RegistryService::initialize` does not reject a zero `admin`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20ServiceConsumer::initialize` (`:72`) and `Tip20TrustService::initialize` (`:90`) both revert `ZeroAddress` on a zero `admin`. `Tip20RegistryService::initialize` (`:127`) grants `DEFAULT_ADMIN_ROLE` unchecked, leaving a proxy nobody can configure or upgrade.

**Recommended Mitigation:** Add the same check to `Tip20RegistryService::initialize`.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.

\clearpage
