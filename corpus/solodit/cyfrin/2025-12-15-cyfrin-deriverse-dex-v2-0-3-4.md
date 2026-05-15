---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Unnecessary Lamports Transfer Without Checking Existing Balance
vuln_class: []
---

# Unnecessary Lamports Transfer Without Checking Existing Balance

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `new_private_client()` function transfers the full `minimum_balance` amount to the `private_clients_acc` account without first checking if the account already has sufficient lamports. This results in unnecessary transfers even when the account already contains enough funds to cover the rent requirement.

```rust
// src/program/processor/new_private_client.rs:163-174
let rent = &Rent::default();
let lamports = rent.minimum_balance(std::mem::size_of::<PrivateClient>());

invoke(
    &system_instruction::transfer(admin.key, private_clients_acc.key, lamports),
    &[
        admin.clone(),
        private_clients_acc.clone(),
        system_program.clone(),
    ],
)
.map_err(|err| drv_err!(err.into()))?;
```

This approach differs from the pattern used consistently throughout the codebase in similar scenarios, which calculate and transfer only the difference needed:

**Impact:** **Potential Over-payment:** If the account already contains more than the minimum required balance, the function still attempts to transfer the full minimum balance amount.

**Recommended Mitigation:** Calculate and transfer only the difference needed, matching the pattern used in other functions like `new_operator()`.

**Deriverse:** Fixed in commit [7091f4](https://github.com/deriverse/protocol-v1/commit/7091f48316d77e6769ee8fddeadd4d3a250ba1e1).

**Cyfrin:** Verified.
