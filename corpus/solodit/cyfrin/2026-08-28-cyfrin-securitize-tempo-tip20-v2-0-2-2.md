---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-2
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
title: '`Tip20RegistryService` events do not expose effective wallet authorization'
vuln_class: []
---

# `Tip20RegistryService` events do not expose effective wallet authorization

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** Registry wallet and lock events describe identity changes, not the final TIP-403 authorization set. In particular, `InvestorFullyUnlocked` can be emitted while wallets staged during the lock remain unauthorized. An indexer cannot reconstruct policy membership from registry events alone.

**Recommended Mitigation:** Document TIP-403 events and direct policy queries as the authorization source of truth. If registry-only reconstruction is required, emit a per-wallet authorization event whenever a policy bit changes and clarify the meaning of `InvestorFullyUnlocked`.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.
