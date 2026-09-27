---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-5
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
title: '`Tip20RegistryService::registerInvestorWithWallets` can retain stale proof
  metadata'
vuln_class: []
---

# `Tip20RegistryService::registerInvestorWithWallets` can retain stale proof metadata

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** Idempotent `Tip20RegistryService::registerInvestorWithWallets` can update an attribute's value and expiry while preserving its existing proof hash. This is correct if the hash identifies independent evidence, but ambiguous if it commits to the prior attribute tuple.

**Recommended Mitigation:** Define what the proof hash attests. If it commits to value or expiry, require a replacement hash whenever those fields change. If it identifies independent evidence, document the preservation behavior explicitly.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.
