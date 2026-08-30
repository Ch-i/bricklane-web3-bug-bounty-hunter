---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: '`change_admin` is single-step and permits irreversible admin loss through
  bad input'
vuln_class: []
---

# `change_admin` is single-step and permits irreversible admin loss through bad input

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** `change_admin` immediately overwrites the stored admin with the supplied `new_admin`. There is no acceptance step, and there is no guard against obviously bad destinations such as the default pubkey or `system_program::ID`.

This is not an exploit against an honest admin, but it is a real operational footgun: a typo or bad integration call can permanently brick future admin operations.

**Recommended Mitigation:** Use a two-step transfer pattern with `pending_admin` plus an explicit `accept_admin` flow, and reject sentinel addresses such as `Pubkey::default()` and `system_program::ID`.

**Securitize:** Acknowledged.
