---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: DS bridge `initialize` accepts zero-value parameters that update instructions
  reject
vuln_class: []
---

# DS bridge `initialize` accepts zero-value parameters that update instructions reject

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The DS bridge `Initialize::handler` does not validate `authorized_user_role` and `executor_program_id` against `ZERO_PUBKEY`, unlike `UpdateAuthorizedUserRole::handler` (line 23) and `UpdateExecutorProgramId::handler` (line 23) which both reject zero. This creates a defense parity gap between initialization and update paths.

**Impact:** Bridge can be initialized in a non-functional state requiring corrective update calls. Escalated to Medium when combined with permissionless init and no ownership transfer (see issue 3).

**Recommended Mitigation:** Add matching zero-value checks in `initialize`:

```rust
require!(authorized_user_role != ZERO_PUBKEY, BridgeError::RbacNotConfigured);
require!(executor_program_id != ZERO_PUBKEY, BridgeError::ZeroExecutorProgramId);
```

**Securitize:** Fixed in [74a75](https://github.com/securitize-io/bc-solana-bridge-sc/commit/74a7511131df7ce1c6e250dfecf3156113f5981f).

DS bridge initialize now rejects zero authorized_user_role (RbacNotConfigured) and zero executor_program_id (ZeroExecutorProgramId), bringing it to parity with update_authorized_user_role / update_executor_program_id

**Cyfrin:** Confirmed.
