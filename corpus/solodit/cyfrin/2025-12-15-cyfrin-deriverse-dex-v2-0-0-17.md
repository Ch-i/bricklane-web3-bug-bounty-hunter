---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing Signer Verification in `voting_reset` Function Allows Unauthorized
  Execution
vuln_class: []
---

# Missing Signer Verification in `voting_reset` Function Allows Unauthorized Execution

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `voting_reset` function in `src/program/processor/voting_reset.rs` only verifies that the `admin` account's public key matches the operator address, but does not verify that the `admin` account is actually a signer of the transaction. **This allows an attacker to execute the `voting reset` instruction by passing account that matches the operator address but no signing is required, resetting critical voting parameters without proper authorization.**

```rust
    let root_state: &RootState = RootState::from_account_info(root_acc, program_id)?;

    if root_state.operator_address != *admin.key {
        bail!(InvalidAdminAccount {
            expected_address: root_state.operator_address,
            actual_address: *admin.key
        })
    }
```

**Impact:** An attacker could execute `voting_reset` without possessing the operator's private key,  resetting critical voting parameters without proper authorization.


**Recommended Mitigation:** Add a signer verification check before the operator address check.

```rust
    if !admin.is_signer {
        bail!(MustBeSigner {
            address: *admin.key
        })
    }
```
**Deriverse:** Fixed in commit [bfc0c96](https://github.com/deriverse/protocol-v1/commit/bfc0c96991d10b19da49c63483999955a810c62b).

**Cyfrin:** Verified
