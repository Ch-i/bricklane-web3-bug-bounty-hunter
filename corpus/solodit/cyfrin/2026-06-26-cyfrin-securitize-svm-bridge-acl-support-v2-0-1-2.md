---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: Missing upfront validation  during initialization
vuln_class: []
---

# Missing upfront validation  during initialization

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** During bridge initialization, SPL token configuration is accepted without fully validating that the SPL mint is controlled by the expected ACL PDA, and without checking that `spl_token_registry_program_id` is non-zero.
The initialization flow only checks that the token config broadly matches the mint type:
```rust
token_config.require_matches_mint(
    &ctx.accounts.asset_mint.to_account_info(),
    &ctx.accounts.mint_authority.to_account_info(),
)?;
```
For SPL tokens, this only confirms the mint is not detected as a DS mint:
```rust
match (self, is_ds_mint) {
    (TokenConfig::Ds { .. }, true) => Ok(()),
    (TokenConfig::Spl { .. }, false) => Ok(()),
    _ => err!(BridgeError::InitParamsMismatch),
}
```
It does not validate that:
```rust
acl_program_id != ZERO_PUBKEY
spl_token_registry_program_id != ZERO_PUBKEY
mint_authority == expected ACL PDA
```
A similar non-zero check exists later when updating the registry program id correctly:
```rust
require!(
    new_spl_token_registry_program_id != ZERO_PUBKEY,
    BridgeError::SplTokenRegistryProgramNotConfigured,
);
```
But the same validation is not enforced during initialization.

**Impact:** This can allow an SPL bridge instance to be initialized with incomplete or incorrect ACL/registry configuration. The issue is mostly defense-in-depth because later bridge/execute paths may fail when they try to use the bad config, but the bridge can still be deployed into a broken state.
This may cause outbound or inbound bridge operations to fail unexpectedly, especially inbound minting, where the ACL program and expected mint authority are required.

**Recommended Mitigation:** Add strict SPL config validation during initialization as well.

**Securitize:** Partially already fixed, remainder is intended design. The two non-zero checks (acl_program_id != 0, spl_token_registry_program_id != 0) are already enforced at initialize — added in audit fix commit [13d365efc](https://github.com/securitize-io/bc-solana-bridge-sc/commit/13d365efc7cfb81069adbbf6e33b8e3ddb9536cd) (the issue text predates that change). The remaining point (mint_authority == expected ACL PDA at init) we keep as-is by design: ACL-PDA correctness is validated lazily at the first ACL CPI, initialize is permissioned to the program upgrade authority (so only the trusted deployer can misconfigure, no third-party exploit), and an upfront check would re-introduce a find_program_address deliberately removed for gas in audit v1.0 issue 17. No further change.

**Cyfrin:** Partial Fix verified. Remainder are marked as acknowledged as by design.
