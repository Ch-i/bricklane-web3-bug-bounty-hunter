---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: '`token_account` is missing a local `mint == mint.key()` constraint in authority
  flows'
vuln_class: []
---

# `token_account` is missing a local `mint == mint.key()` constraint in authority flows

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** The authority's `freeze_account`,  `thaw_account`, and the `mint_to_checked` instructions do not locally enforce that the provided token account belongs to the supplied mint. Downstream Token-2022 or Token-ACL checks should still reject mismatches, so the issue is primarily defense-in-depth and error-surface quality rather than a direct exploit.

**Recommended Mitigation:** Add an explicit local `token_account.mint == mint.key()` constraint to each affected instruction context.

**Securitize:** Fixed in [f65f393](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/f65f393be9d5f5a1d6a20a770dec058216f8780c).

**Cyfrin:** Verified.
