---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: '`change_points_program_expiration` is permissionless'
vuln_class: []
---

# `change_points_program_expiration` is permissionless

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `change_points_program_expiration` function fails to verify that the `admin` account has actually signed the transaction. While the function checks that the provided admin account key matches the expected `operator_address` in the root state, it does not verify that the account is a signer using `admin.is_signer`. The comment indicates that the admin should be a signer (// [*`create_account` can be dosed with pre-funding*](#createaccount-can-be-dosed-with-prefunding) - Admin (Signer)), but this requirement is not enforced in the code so any normal user can pass admin pubkey and execute this instruction without even real admin signing it.
```rust
// Only checks that the admin key matches, but not checking if the admin has actually signed the transaction;
if root_state.operator_address != *admin.key {
    bail!(InvalidAdminAccount {
        expected_address: root_state.operator_address,
        actual_address: *admin.key,
    });
}
// Missing: if !admin.is_signer { ... }
```
**Impact:** Unauthorised access to supposiely admin gated functionality.

**Recommended Mitigation:** Make sure the `admin` adress not only matches the stored address but also is the signer
```rust
    if !admin.is_signer {
        bail!(InvalidAdminAccount {
            expected_address: root_state.operator_address,
            actual_address: *admin.key,
        });
    }
```
**Deriverse:** Fixed in commit: [8a479a](https://github.com/deriverse/protocol-v1/commit/8a479a06d86536deeb65eeeb2379df5520ba4595)

**Cyfrin:** Verified.
