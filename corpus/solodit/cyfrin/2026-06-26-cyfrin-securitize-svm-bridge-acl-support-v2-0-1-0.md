---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: '`securitize_bridge` inbound SPL resolver hardcodes the Token-2022 program
  for ATA derivation, breaking inbound delivery for a classic-SPL-Token mint configured
  as `TokenConfig::Spl`'
vuln_class: []
---

# `securitize_bridge` inbound SPL resolver hardcodes the Token-2022 program for ATA derivation, breaking inbound delivery for a classic-SPL-Token mint configured as `TokenConfig::Spl`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** The executor resolver for the SPL inbound path unconditionally derives the recipient associated token account (and the `token_program` account meta) using the Token-2022 program id:

```rust
let token_program = anchor_spl::token_2022::ID;
let recipient_token_account = get_associated_token_address_with_program_id(
    destination_wallet, asset_mint, &token_program,
);
```

By contrast, the `execute_vaa_v1_spl` and `bridge_spl_tokens` handlers take `token_program: Interface<'info, TokenInterface>` and bind the ATA to `associated_token::token_program = token_program`, i.e. they accept whichever token program actually owns the mint. The `TokenConfig::Spl` variant is detected at `initialize` purely by the mint authority NOT being owned by the asset controller (the false branch of the DS-mint check); nothing pins an SPL-variant mint to the Token-2022 program specifically.

If an operator configures an `Spl` bridge for a mint owned by the classic SPL Token program, every executor-driven inbound relay derives the recipient ATA under Token-2022 - a different address than the real classic-SPL ATA the mint expects. When the resolved account list is fed into `execute_vaa_v1_spl`, the `asset_mint` (`InterfaceAccount<Mint>`) deserialize requires the mint's owner to equal the supplied `token_program` (Token-2022), but the mint is owned by classic SPL Token, so account resolution fails and the inbound path for that mint cannot execute via the standard executor flow. The fault manifests under honest configuration - no malicious actor is required - but only for an SPL-configured mint that is classic SPL Token rather than Token-2022.

**Files:**

- `securitize_bridge::derive_execute_vaa_accounts_spl` - `bc-solana-bridge-sc/programs/securitize_bridge/src/resolver/spl.rs:126-132`

**Impact:** The standard executor-driven inbound path is broken for any `Spl`-configured mint that is a classic SPL Token rather than Token-2022: the resolver builds an account list whose recipient ATA and `token_program` meta are derived under Token-2022, which `execute_vaa_v1_spl` then rejects when it deserializes the classic-SPL `asset_mint`. The direct `execute_vaa_v1_spl` instruction itself is not inherently broken - its handler binds the ATA to the caller-supplied `token_program`, so a manual submission with the correct classic-SPL token program and matching ATA can still execute - but the automated executor relay (which uses this resolver) cannot deliver. No value is lost: the VAA is simply never consumed on the failed path (the `consumed_vaa` replay PDA is created with `init` and is only written on a successful instruction), so the burned source tokens remain redeemable via a correctly-constructed manual `execute_vaa_v1_spl` and the failure fails closed. Because the SPL product is documented as Token-2022-only, the realistic blast radius is a misconfiguration-class denial of the automated inbound path for the affected instance, with no value loss.

**Recommended Mitigation:** Derive the recipient ATA's token program from the live mint account's owner rather than hardcoding the Token-2022 program. In the resolver, read the `asset_mint` account's owner and pass that program id into `get_associated_token_address_with_program_id` and the `token_program` account meta, so the resolved ATA matches the address the handler derives. Alternatively, pin the SPL variant to Token-2022 explicitly at `initialize` (assert the mint account owner equals the Token-2022 program for `TokenConfig::Spl`) so the resolver hardcode and the config are provably consistent.

**Securitize:** Fixed in commit [cd5026d](https://github.com/securitize-io/bc-solana-bridge-sc/commit/cd5026db5a0ce932d6201baf87a2299eaa9fb897). Fixed via the second recommended option, aligned with the documented Token-2022-only design. initialize now pins the SPL variant to Token-2022: for TokenConfig::Spl it asserts the asset_mint account owner equals the Token-2022 program (SplMintNotToken2022), so the resolver's hardcoded Token-2022 ATA derivation and the stored config are provably consistent. This makes the misconfiguration fail-fast at deploy time — an operator can no longer create an SPL instance over a classic-SPL mint — rather than silently breaking the automated inbound path later.

**Cyfrin:** Verified.
