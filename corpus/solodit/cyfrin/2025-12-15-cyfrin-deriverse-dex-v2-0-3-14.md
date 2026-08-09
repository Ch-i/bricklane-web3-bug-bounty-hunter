---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-14
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing System Program Check in Instructions like `new_operator`(Inconsistency)
vuln_class: []
---

# Missing System Program Check in Instructions like `new_operator`(Inconsistency)

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Unlike many other handlers, `new_operator` does not verify that the `system_program` account equals `solana_program::system_program::ID` before using it in `realloc_account_data`. The call would eventually fail if a wrong account is supplied, but the error surfaces only after a CPI panic rather than as a clean, descriptive failure.

The instruction expects `system_program (accounts[3])` to be the Solana system program and later passes it into `realloc_account_data`, which performs a CPI to the system program.

```rust
    let system_program = next_account_info!(accounts_iter)?;
    check_holder_admin(admin)?;
    let mut holder_state = HolderState::new(holder_acc, program_id)?;

    let begin = std::mem::size_of::<HolderAccountHeader>()
        + (holder_state.header.operators_count as usize) * std::mem::size_of::<Operator>();

    let new_size = begin + std::mem::size_of::<Operator>();

    if holder_acc.data_len() < new_size {
        realloc_account_data(admin, holder_acc, system_program, new_size, None, true)
            .map_err(|err| drv_err!(err.into()))?;
    }
```

 If a client provides some other executable account, the CPI will trap because the runtime detects the program-id mismatch. This isn’t exploitable, but it differs from other processors (e.g., `new_instrument`) that proactively check `system_program.key == system_program::ID` and return a clear error before the CPI.

```rust
    if !system_program::check_id(system_program.key) {
        bail!(InvalidSystemProgramId {
            actual_address: *system_program.key,
        });
    }
```


**Impact:** Program will panic instead of returning a well-typed error.

**Recommended Mitigation:** Add an explicit check in `new_operator` (and any similar handlers) that `system_program.key == &solana_program::system_program::ID`

**Deriverse:** Fixed in commit [d7b852b4](https://github.com/deriverse/protocol-v1/commit/d7b852b42564541dddec86289a23ac2696b264af).

**Cyfrin:** Verified.
