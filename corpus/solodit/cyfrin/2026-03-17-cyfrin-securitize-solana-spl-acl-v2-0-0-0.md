---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: Permissionless freeze setup is wired to the thaw extra-metas PDA instead of
  the freeze PDA
vuln_class: []
---

# Permissionless freeze setup is wired to the thaw extra-metas PDA instead of the freeze PDA

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** The program exposes only one extra-metas seed, `thaw_extra_account_metas`, in `constants.rs`, and `setup_extra_metas` can only initialize a PDA derived from that thaw seed. The local SDK mirrors that assumption: `extraMetasPda()` always derives `["thaw_extra_account_metas", mint]`, and the `freezePermissionless` builder passes that same PDA in the remaining accounts for permissionless freeze.

```rust
  /// CHECK: Extra metas pda account checking in gating program
  #[account(
      mut,
      seeds = [constants::THAW_EXTRA_ACCOUNT_METAS_SEED, mint.key().as_ref()],
      bump,
      seeds::program = gating_program.key()
  )]
  pub extra_metas: AccountInfo<'info>,
```

```rust
#[constant]
pub const THAW_EXTRA_ACCOUNT_METAS_SEED: &[u8] = b"thaw_extra_account_metas";
```

However, the vendored Token-ACL interface and SDK clearly model two distinct validation accounts:

- thaw uses `["thaw_extra_account_metas", mint]`
- freeze uses `["freeze_extra_account_metas", mint]`

This is not just a naming difference in the client code. Token-ACL's on-chain `invoke_can_freeze_permissionless` helper computes the freeze-side PDA with `get_freeze_extra_account_metas_address(...)` and only loads extra account metadata if that exact freeze PDA is present in `additional_accounts`. If the caller instead supplies the thaw PDA, the freeze helper does not treat it as the validation account and does not resolve the freeze-side extra account dependencies from it.

As a result, the current integration path is miswired:

1. `setup_extra_metas` only prepares the thaw-side validation account.
2. `freezePermissionless` still forwards that thaw-side account during freeze.
3. Token-ACL freeze resolution expects the freeze-side account and ignores the thaw-side one for dependency expansion.

**Impact:** Permissionless thaw can be configured correctly, but permissionless freeze is only reliable for trivial gate programs that require no freeze-side extra metas. Any gate that follows the standard freeze interface and depends on `freeze_extra_account_metas` for account resolution will fail to receive its expected dependency set and may revert at runtime.

**Recommended Mitigation:** Add a distinct freeze extra-metas seed and setup flow on the on-chain side, then update the SDK so:

- thaw derives and supplies `thaw_extra_account_metas`
- freeze derives and supplies `freeze_extra_account_metas`

**Securitize:** Fixed in [4794d46](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/4794d460604e2967605d29d8535829f130caddb9).

**Cyfrin:** Verified.

\clearpage
