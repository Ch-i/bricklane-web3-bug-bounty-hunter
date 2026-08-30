---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-10
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Router admin can repoint an existing router to an unrelated Jump pool
vuln_class: []
---

# Router admin can repoint an existing router to an unrelated Jump pool

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** `update_jump_pool_config_handler` allows the router admin to replace the full `JumpPoolConfig`, including the underlying pool address, as long as the new config validates against the provided pool state.

There is no invariant that the new pool address must match the router’s existing pool address. As a result, a router that was initialized for one BisonFi pool can later be repointed to another valid pool, potentially one that was expected to be served by a different router.

**Impact:** This creates configuration ambiguity and weakens router-to-pool isolation assumptions. Operators, users, indexers, or off-chain systems may treat a router as the canonical gateway for a specific pool, but the admin can change that router to execute swaps against a different pool without creating a new router.

**Recommended Mitigation:** If routers are intended to be bound to a single pool, make the pool address immutable after initialization. In `update_jump_pool_config_handler`, require the new config address to equal the current config address:
```rust
require!(
    jump_pool_config.address == jump_router_state.jump_pool_config.address,
    JumpRouterError::InvalidJumpPoolConfig
);
```

**Securitize:** Acknowledged.
