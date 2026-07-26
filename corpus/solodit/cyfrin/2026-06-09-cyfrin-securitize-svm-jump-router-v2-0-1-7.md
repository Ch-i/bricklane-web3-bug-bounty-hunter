---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-7
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
title: Standard `execute_swap` accepts an empty regulatory `external_id`
vuln_class: []
---

# Standard `execute_swap` accepts an empty regulatory `external_id`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The standard backend/operator-gated `execute_swap` instruction accepts `external_id: String` as an instruction argument but never validates that it is non-empty or otherwise well-formed:

- `programs/bc-solana-jump-router-sc/src/lib.rs:94-112`
- `programs/bc-solana-jump-router-sc/src/instructions/operator/execute_swap.rs:20-55`

The value is forwarded unchanged into the shared swap implementation and emitted as the only business identifier in the `PstRamp` event on both directions (`swap_accounts.rs:410-420`, `swap_accounts.rs:600-610`, schema at `events.rs:98-108`).

The headless path intentionally uses an empty external id:

```rust
pub const SWAP_HEADLESS_EXTERNAL_ID: &str = "";
```

That matches what was stated in the kickoff meeting, which describe headless swaps as deliberately removing reporting features such as the external IDs used for regulatory tracking. The gap is that the standard MBBO/backend-authorized path has the same capability: an operator can submit `execute_swap` with `external_id == ""`, and the router will execute the swap and emit an authoritative `PstRamp` record with a blank regulatory identifier — without going through the explicit headless path.

**Recommended Mitigation:** Reject blank standard external IDs before any swap execution:

```rust
require!(!external_id.trim().is_empty(), JumpRouterError::InvalidExternalId);
require!(external_id.len() <= MAX_EXTERNAL_ID_LEN, JumpRouterError::InvalidExternalId);
```

**Securitize:** Fixed in [35220bb](https://github.com/securitize-io/bc-bd-router-sc/commit/35220bb9df25c77386192846a1b9a3329c8e7ff3).

**Cyfrin:** Verified.
