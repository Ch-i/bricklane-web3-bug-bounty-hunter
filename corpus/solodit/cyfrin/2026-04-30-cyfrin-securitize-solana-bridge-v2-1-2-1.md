---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Permissionless `initialize` combined with no ownership transfer and zero-value
  acceptance enables permanent bridge hijacking
vuln_class: []
---

# Permissionless `initialize` combined with no ownership transfer and zero-value acceptance enables permanent bridge hijacking

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:**
1. Both `initialize` instructions accept any `Signer` as owner with no restriction to a known deployer
2. The DS bridge `initialize` does not validate `authorized_user_role` and `executor_program_id` against zero, unlike the `update` instructions which reject `ZERO_PUBKEY`
3. Neither program has an ownership transfer mechanism

An attacker who front-runs initialization with `authorized_user_role = Pubkey::default()` and `executor_program_id = Pubkey::default()` permanently owns and permanently disables the bridge instance for that mint. The config PDA uses Anchor `init` (one-shot), so re-initialization is impossible. Both `bridge_ds_tokens` and `execute_vaa_v1` check `config.authorized_user_role != ZERO_PUBKEY` and revert with `BridgeError::RbacNotConfigured`.

**Impact:** Permanent denial-of-service for a specific DS token or USDC bridge instance. The legitimate team cannot recover ownership and must redeploy the entire program with a new program ID, requiring re-integration with Wormhole, the executor, and EVM-side bridge contracts. On Solana, front-running is harder than EVM (QUIC-based TPU reduces mempool visibility) but remains feasible via validator-side observation.

**Proof of Concept:**
1. Securitize team deploys the program and plans to initialize bridge for DS token mint X
2. Attacker monitors for the `initialize` transaction and submits competing tx with higher priority fee: `owner = attacker_wallet`, `authorized_user_role = Pubkey::default()`, `executor_program_id = Pubkey::default()`
3. Attacker's tx lands first; `BridgeConfig` PDA created with attacker as owner and zero config values
4. Legitimate team's `initialize` tx fails (PDA already exists)
5. No `transfer_ownership` instruction exists; legitimate team cannot reclaim the config
6. All bridge operations revert: `bridge_ds_tokens` checks `authorized_user_role != ZERO_PUBKEY` (line 43)
7. The bridge is permanently non-functional for mint X

**Recommended Mitigation:**
1. Add access control to `initialize`: require `owner.key() == DEPLOYER_PUBKEY` or use a program-level deployer authority
2. Add zero-value validation in `initialize` matching the update instructions:
```rust
require!(authorized_user_role != ZERO_PUBKEY, BridgeError::RbacNotConfigured);
require!(executor_program_id != ZERO_PUBKEY, BridgeError::ZeroExecutorProgramId);
```
3. Add a two-step ownership transfer: `propose_owner` + `accept_ownership`

**Securitize:** Fixed in [7d3cc0a](https://github.com/securitize-io/bc-solana-bridge-sc/commit/7d3cc0a3b73a88e3f056c3e2f1cccb420015975e).

**Cyfrin:** Verified.
