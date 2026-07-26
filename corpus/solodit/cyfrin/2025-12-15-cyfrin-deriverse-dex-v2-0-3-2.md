---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Transfers are noop when `lamports_diff`  is zero
vuln_class: []
---

# Transfers are noop when `lamports_diff`  is zero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The codebase contains multiple instances where lamports transfers are performed for rellocating space and size without checking if the transfer amount `lamports_diff` is greater than zero. To evaluate `lamports_diff` we are using `saturating_sub` which limits subtraction in cases when there are chances of underflow.
```rust
// here if the account already had enough lamports to cover up its rent, the `lamports_diff` would come out as 0.
let lamports_diff = new_minimum_balance.saturating_sub(account.lamports());
invoke(
    &system_instruction::transfer(signer.key, account.key, lamports_diff),
    &[signer.clone(), account.clone(), system_program.clone()],
)?;
```
When `lamports_diff` is zero, the code still makes unnecessary Cpi calls to the System Program's transfer instruction, which wastes computational units and is no op.

Here are the files where its present: `perp_engine.rs`, `new_base_crncy.rs`, `new_operator.rs`, `engine.rs`, `candles.rs`, `client_community.rs`, `client_primary.rs`

**Impact:** Unnecessary cu lost in cases when `lamports_diff`==0.

**Recommended Mitigation:** Perform transfer only if `lamports_diff` > 0.
```rust
let lamports_diff = new_minimum_balance.saturating_sub(account.lamports());
if lamports_diff > 0 {
    invoke(
        &system_instruction::transfer(signer.key, account.key, lamports_diff),
        &[signer.clone(), account.clone(), system_program.clone()],
    )?;
}
```
**Deriverse:** Fixed in commit: [7091f4](https://github.com/deriverse/protocol-v1/commit/7091f48316d77e6769ee8fddeadd4d3a250ba1e1)

**Cyfrin:** Verified.
