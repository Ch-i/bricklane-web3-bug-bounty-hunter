---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: Redundant Zero-Address Check in `revoke_operator`
vuln_class: []
---

# Redundant Zero-Address Check in `revoke_operator`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** The `operator != Pubkey::default()` check in `revoke_operator_handler` is redundant. Since `add_operator_handler` already prevents the zero address from being added to the operators list, it can never be present when revoking. The subsequent `state.operators.contains(&operator)` check will always fail for `Pubkey::default()` with `OperatorNotFound`, yielding the same outcome.


In `revoke_operator_handler`:

```rust
require!(
    operator != Pubkey::default(),
    VaultRegistrarError::InvalidOperator
);

require!(
    state.operators.contains(&operator),
    VaultRegistrarError::OperatorNotFound
);
```

In `add_operator_handler`, the zero address is already rejected:

```rust
require!(
    new_operator != Pubkey::default(),
    VaultRegistrarError::InvalidOperator
);
// ...
state.operators.push(new_operator);
```

Therefore, `Pubkey::default()` can never exist in `state.operators`. For `operator == Pubkey::default()`, `contains()` will return false and the handler will revert with `OperatorNotFound` regardless of the first check.

**Impact:**
- Redundant code increases maintenance burden.

**Recommended Mitigation:** Remove the redundant `operator != Pubkey::default()` check from `revoke_operator_handler`. Rely on `state.operators.contains(&operator)` to reject invalid operators, including the zero address.

**Securitize:** Fixed in [00d1f81](https://github.com/securitize-io/bc-solana-whitelister/commit/00d1f819c638d9495aab46ebf54e1a3be5c97017).

**Cyfrin:** Verified.

\clearpage
