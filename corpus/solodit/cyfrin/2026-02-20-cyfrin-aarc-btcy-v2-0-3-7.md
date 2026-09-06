---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Redundant `DEFAULT_ADMIN_ROLE` grant in `AllowList::__AllowList_init`
vuln_class: []
---

# Redundant `DEFAULT_ADMIN_ROLE` grant in `AllowList::__AllowList_init`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `AllowList::__AllowList_init` grants `DEFAULT_ADMIN_ROLE` to `admin`, but the calling initializers also grant `DEFAULT_ADMIN_ROLE` to the same `admin`. This duplicates role setup work during initialization.

Consider removing one of the duplicate `DEFAULT_ADMIN_ROLE` grants (preferably keep the role assignment in a single place, either in `__AllowList_init` or in the top-level initializers to avoid redundant storage writes/checks.

**Aarc:** Fixed in commit [93f86f4](https://github.com/aarc-xyz/btcy-contracts-main/commit/93f86f47a1a0f7d549ebe3e5e3106f90d76722c2).

**Cyfrin:** Verified.
