---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: '`InvestorRegistry::load` skips the Anchor discriminator check before Borsh-deserializing
  the whitelist account body'
vuln_class: []
---

# `InvestorRegistry::load` skips the Anchor discriminator check before Borsh-deserializing the whitelist account body

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** On the inbound SPL path the bridge reads the external whitelist record through `InvestorRegistry::load`. The loader borrows the account data, requires only that `data.len() >= 8`, then skips the first 8 bytes and Borsh-deserializes the `mint`, `wallet`, `investor_id`, and `bump` fields from the remainder. It never compares those leading 8 bytes against the Anchor discriminator `sha256("account:InvestorRegistry")[..8]`, so the account *type* is never verified at deserialization time:

```rust
let mut slice = &data[ANCHOR_DISCRIMINATOR_LEN..];
let view = Self::deserialize(&mut slice)
    .map_err(|_| error!(BridgeError::InvalidInvestorRegistry))?;
```

This is currently not exploitable. In `execute_vaa_v1_spl` and `bridge_spl_tokens` the `investor_registry` account is an `UncheckedAccount` pinned by Anchor `seeds = [INVESTOR_REGISTRY_SEED_PREFIX, asset_mint, wallet]`, `seeds::program = <configured registry program>`, and `owner = <configured registry program>`. The registry program creates only `InvestorRegistry`-typed accounts at that seed prefix, and the `owner` constraint already rejects system-owned, zero-lamport, or closed accounts. So a type-confusion or zeroed-account read is not reachable today; the address and owner pins do the work the discriminator check would otherwise do. . This is the only registry-read step that does not enforce the account type by its discriminator.

**Files:**

- `securitize_bridge::InvestorRegistry::load` - `bc-solana-bridge-sc/programs/securitize_bridge/src/state/investor_registry.rs:38-57`

**Impact:** No impact under the current single-account-type registry program and the seeds/owner pinning - the missing check is defense-in-depth, not a live vulnerability. It becomes a real type-confusion vector only if the registry program is later extended to own a second account type derivable at a colliding seed prefix, or if the bridge's configured registry program id is repointed to a program with a different account layout: in either case the body would be parsed as an `InvestorRegistry` from raw bytes with no discriminator gate, and a non-registry account could satisfy the whitelist check. The fix is cheap and removes the latent exposure while restoring parity with the DS path.

**Recommended Mitigation:** In `load`, before deserializing the body, assert the leading 8 bytes equal the expected Anchor discriminator for the `InvestorRegistry` account, mirroring the existing DS-path check in `load_imr_investor`. Compute the discriminator as `sha256("account:InvestorRegistry")[..8]` (or reference the whitelist program's published constant) and `require!` equality before reading `data[8..]`, returning `BridgeError::InvalidInvestorRegistry` on mismatch.

**Securitize:** Fixed in commit [394be0f](https://github.com/securitize-io/bc-solana-bridge-sc/commit/394be0f82e325b855601178963f7bc5c2da103a8). InvestorRegistry::load now asserts the leading 8 bytes equal the Anchor discriminator sha256("account:InvestorRegistry")[..8] (require!(data.starts_with(&INVESTOR_REGISTRY_DISCRIMINATOR), InvalidInvestorRegistry)) before Borsh-deserializing the body, restoring parity with the DS path's load_imr_investor and removing the latent type-confusion exposure. A test also locks the hardcoded discriminator constant to the value Anchor derives.

**Cyfrin:** Verified.
