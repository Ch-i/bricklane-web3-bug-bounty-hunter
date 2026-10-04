---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20TrustService::setServiceOwner` can assign `MASTER` to an inert address'
vuln_class: []
---

# `Tip20TrustService::setServiceOwner` can assign `MASTER` to an inert address

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20TrustService::setServiceOwner` writes `MASTER` without applying the protocol-address exclusions used by `setRole`. The current owner can transfer control to the token, registry, trust proxy, or another inert contract.

**Impact:** After the outgoing owner is demoted, no externally controlled account may be able to manage roles or upgrade the trust and consumer proxies.

**Recommended Mitigation:** Apply the same invalid-target checks to ownership transfer and use a two-step handoff in which the proposed owner must accept before the current owner is demoted.

**Securitize:** Fixed in [PR 16](https://github.com/securitize-io/bc-tempo-sc/pull/16/changes/670b1ac659f38ae71a915988077ccc7037c02054#diff-c7d4a772c30d24581cb1be0a0df4acaca708c5a0005bd337486ebe821192adcc).

**Cyfrin:** Verified.
