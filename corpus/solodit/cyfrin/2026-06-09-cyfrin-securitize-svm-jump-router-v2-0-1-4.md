---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: '`JumpRouterCounter` uses `init_if_needed` with a fixed singleton seed'
vuln_class: []
---

# `JumpRouterCounter` uses `init_if_needed` with a fixed singleton seed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The `jump_router_counter` PDA is initialized with `init_if_needed` using the fixed seed `[JUMP_ROUTER_COUNTER_SEED]` (`programs/bc-solana-jump-router-sc/src/instructions/admin/initialize.rs:88-95`). Each call to `initialize_handler` reads the current counter value, creates a new router state at `[JUMP_ROUTER_STATE_SEED, counter.to_le_bytes()]`, then increments the counter (`initialize.rs:131-154`).

If an operator pre-derives and pre-signs an initialize transaction when the counter is `N`, and another allowed initializer lands an initialize transaction first, the counter advances to `N + 1`. The pre-signed transaction still targets the state PDA for counter `N`, which now exists, so the `init` constraint fails with an account-already-in-use error.

**Impact:** The pre-signed initialize transaction becomes invalid and must be rebuilt with the new counter value. Recovery is straightforward, so no funds are at risk and no permanent state is corrupted. The impact is an unexpected initialization failure for offline/pre-signed initialization flows.

**Recommended Mitigation:** Document that initialize transactions must derive the target router state from the live counter immediately before signing. If the program does not need multiple router instances, remove the counter and use a fixed singleton state PDA.

**Securitize:** Fixed in [8cb8e4d](https://github.com/securitize-io/bc-bd-router-sc/commit/8cb8e4d5e1ab6ab144486861e6c02a8b0f07120c).

**Cyfrin:** Verified.
