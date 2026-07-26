---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Better storage packing
vuln_class: []
---

# Better storage packing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Better storage packing, assuming already deployed contracts won't be upgraded as these changes require fresh deployment:
* `IBTCYHub::IBTCYHubStorage` declare `subscriptionPaused, redemptionPaused` after `complianceAddress`

**Aarc:** Fixed in commit [abe76b8](https://github.com/aarc-xyz/btcy-contracts-main/commit/abe76b8d3c98cc9672df2988892c5b27c5f59cff).

**Cyfrin:** Verified.
