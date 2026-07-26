---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-4-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Remove `from` parameter from `Minter:redeem` and `_onlySender` function
vuln_class: []
---

# Remove `from` parameter from `Minter:redeem` and `_onlySender` function

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `Minter:redeem` takes a `from` input parameter but then calls `_onlySender` to enforce that `from == msg.sender`.

In this case there is no need for the `from` input parameter for the `_onlySender` function; remove them both and just use `msg.sender` inside `Minter:redeem`.

**Syntetika:**
Fixed in commit [94a2165](https://github.com/SyntetikaLabs/monorepo/commit/94a21650ac63be3d22c545e629ca0283d9664872).

**Cyfrin:** Verified.
