---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: Redundant executable check for token ACL program after address validation
vuln_class: []
---

# Redundant executable check for token ACL program after address validation

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** Throughout the codebase, when validating the Token ACL program account, the code performs both an address validation check against the hardcoded `TOKEN_ACL` constant and an `executable` check. Once the address is verified to match a known deployed program ID, the executable check becomes redundant and wastes compute units.

A deployed program on Solana at a specific address is inherently executable - the address validation alone is sufficient to ensure the account is the correct Token ACL program

**Impact:** Each redundant `executable` check consumes extra compute units which is completely unnecessary because it does not add extra security.

**Recommended Mitigation:** The address check against `TOKEN_ACL` constant is sufficient since a deployed program at that address must be executable, remove redundant `executable` check from all places. Here are the instances:
1. create_config.rs
2. delete_config.rs
3. freeze_permissionless.rs
4. set_gating_program.rs
5. thaw_permissionless.rs
6. toggle_permissionless.rs
7. freeze_account.rs
8. thaw_account.rs
9. set_authority.rs

**Securitize:** Fixed in [40ed16f](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/40ed16ff5076688f61f9b18387cd3f17ae81ad95).

**Cyfrin:** Verified.

\clearpage
