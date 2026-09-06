---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-0-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: '`securitize_bridge::initialize` applies no validation to the SPL `acl_program_id`,
  permanently bricking an instance from a zero or garbage value'
vuln_class: []
---

# `securitize_bridge::initialize` applies no validation to the SPL `acl_program_id`, permanently bricking an instance from a zero or garbage value

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** `initialize` validates the `Ds` variant's `authorized_user_role` against the zero pubkey but applies NO validation to the `Spl` variant's two stored program ids. `token_config` is taken verbatim from caller instruction data and stored directly as `BridgeConfig::token_config`; for a `TokenConfig::Spl { acl_program_id, spl_token_registry_program_id }` the only structural check performed is `require_matches_mint`, which inspects the mint authority structure, not the two config program ids:

```rust
if let TokenConfig::Ds { authorized_user_role } = &token_config {
    require_keys_neq!(*authorized_user_role, ZERO_PUBKEY, BridgeError::RbacNotConfigured);
}
// no equivalent check for the Spl variant
```

Both SPL program ids can therefore be initialized to `Pubkey::default` or any garbage value. This is asymmetric with the `Ds` variant's own init check, with the consumer instructions `execute_vaa_v1_spl` and `bridge_spl_tokens` (whose account constraints reject a zero registry program id at runtime), and with the setter `update_spl_token_registry_program_id` (which rejects the zero pubkey). The `spl_token_registry_program_id` half is recoverable post-init via that setter, but there is no setter anywhere in the program for `acl_program_id` - the only writes to it are in `initialize` itself and in `update_spl_token_registry_program_id`, the latter preserving the existing `acl_program_id` unchanged. An `acl_program_id` written wrong at init is therefore an irreversible deploy action for that bridge instance.

With a wrong `acl_program_id` stored, every inbound mint reverts: `execute_vaa_v1_spl` calls `require_spl_matching` against the real ACL program account the relayer passes, which never equals the wrong stored value, yielding `InvalidAclProgram`. No instruction can rewrite `acl_program_id`, and because `BridgeConfig` is a per-mint PDA created with `init`, the operator cannot re-`initialize` over it (the second `init` fails - the PDA already exists). Recovery requires a program upgrade or operating a different asset mint. Only the program upgrade authority can call `initialize`, so this harm materializes only when that trusted operator mis-enters the value.

**Files:**

- `securitize_bridge::initialize` - `bc-solana-bridge-sc/programs/securitize_bridge/src/instructions/admin/initialize.rs:118-133`

**Impact:** A fresh SPL bridge instance whose `acl_program_id` was mis-entered at deploy time is permanently non-functional for the inbound EVM-to-Solana mint path, with no on-chain recovery short of a program upgrade. No funds are lost - inbound simply reverts and the outbound burn path is independent of `acl_program_id` - so this is a deploy-time footgun and availability gap rather than a value loss. The `spl_token_registry_program_id` half of the same missing-validation gap is fully recoverable via its setter, so only `acl_program_id` carries the irreversibility.

**Recommended Mitigation:** In `initialize`, extend the `token_config` validation to the `Spl` branch symmetric with the existing `Ds` branch, rejecting a zero `acl_program_id` and a zero `spl_token_registry_program_id`:

```rust
if let TokenConfig::Spl { acl_program_id, spl_token_registry_program_id } = &token_config {
    require_keys_neq!(*acl_program_id, ZERO_PUBKEY, BridgeError::InvalidAclProgram);
    require_keys_neq!(*spl_token_registry_program_id, ZERO_PUBKEY, BridgeError::SplTokenRegistryProgramNotConfigured);
}
```

Separately, consider adding an `update_acl_program_id` setter (mirroring `update_spl_token_registry_program_id`) so that a mis-entered `acl_program_id` is recoverable without a program upgrade.

**Securitize:** Fixed in commit [13d365efc](https://github.com/securitize-io/bc-solana-bridge-sc/commit/13d365efc7cfb81069adbbf6e33b8e3ddb9536cd). initialize now validates the Spl branch symmetrically with the Ds branch — it rejects a zero acl_program_id (InvalidAclProgram) and a zero spl_token_registry_program_id (SplTokenRegistryProgramNotConfigured). Additionally, an update_acl_program_id setter was added (mirroring update_spl_token_registry_program_id) so a mis-entered acl_program_id is recoverable without a program upgrade, removing the irreversibility.

**Cyfrin:** Verified.
