---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-1-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Source-Chain Transfer-Hook Policies Are Bypassed by the Bridge Burn/Remint
  Path
vuln_class: []
---

# Source-Chain Transfer-Hook Policies Are Bypassed by the Bridge Burn/Remint Path

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** DS mints in the Securitize RWA stack are created with a Token-2022 `TransferHook` that points at the Policy Engine program in [create.rs:44](https://github.com/securitize-io/rwa-token/blob/8b0b098f66925f90fe6a0a225cd951da730feea8/programs/asset_controller/src/instructions/create.rs#L44-L59):

```rust
// asset_controller/create.rs
#[account(
    init,
    signer,
    payer = payer,
    // ...
    extensions::transfer_hook::program_id = policy_engine::id(),
    // ...
)]
pub asset_mint: Box<InterfaceAccount<'info, Mint>>,
```

Under normal Token-2022 operation, transfer-specific policy checks run through the transfer hook and enforce rules such as `TransactionAmountLimit`, `TransferPause`, `BlockFlowbackEndTime`, and -- for non-self transfers -- `ForceFullTransfer`, `ForbiddenIdentityGroup`, and sender-side balance rules in [execute.rs:153](https://github.com/securitize-io/rwa-token/blob/8b0b098f66925f90fe6a0a225cd951da730feea8/programs/policy_engine/src/instructions/execute.rs#L153) and [engine.rs:476](https://github.com/securitize-io/rwa-token/blob/8b0b098f66925f90fe6a0a225cd951da730feea8/programs/policy_engine/src/state/engine.rs#L476):

```rust
// policy_engine/engine.rs - enforce_policy()
for policy in self.policies.iter() {
    match &policy.policy_type {
        PolicyType::IdentityApproval => { /* identity filter check */ }
        PolicyType::TransactionAmountLimit { limit } => { /* per-tx amount cap */ }
        PolicyType::TransferPause => { /* global or filtered transfer freeze */ }
        PolicyType::ForceFullTransfer => { /* all-or-nothing transfer rule */ }
        PolicyType::ForbiddenIdentityGroup => { /* blocked identity groups */ }
        PolicyType::MaxBalance { limit } => { /* destination balance cap */ }
        PolicyType::MinBalance { limit } => { /* source/dest minimum balance */ }
        // ...
    }
}
```

The bridge does not use that transfer path. Outbound bridging in `bridge_ds_tokens.rs:298` performs only a custom lock/hold check via `locked_tokens.rs:17`, then burns through the RBAC/asset-controller revoke flow in `revoke.rs:47`:

```rust
// bridge_ds_tokens.rs
// Only check: lock-period constraint
locked_tokens::validate_locked_tokens(
    &ctx.accounts.tracker_account.to_account_info(),
    &ctx.accounts.policy_engine.to_account_info(),
    identity.country,
    balance,
    amount,
    ctx.accounts.clock.unix_timestamp,
)?;

// Then burn directly via RBAC revoke — no transfer_checked, no transfer hook
invoke_revoke_tokens_cpi(
    &ctx,
    amount,
    bridge_authority_bump,
    // ...
)?;
```

The revoke path calls `burn` on the Token-2022 program using the Asset Controller's permanent delegate authority, which does not trigger the transfer hook:

```rust
// asset_controller/revoke.rs
fn burn_tokens(&self, amount: u64, signer_seeds: &[&[&[u8]]]) -> Result<()> {
    let accounts = Burn {
        mint: self.asset_mint.to_account_info(),
        authority: self.asset_controller.to_account_info(),
        from: self.revoke_token_account.to_account_info(),
    };
    let cpi_ctx = CpiContext::new_with_signer(
        self.token_program.to_account_info(),
        accounts,
        signer_seeds,
    );
    burn(cpi_ctx, amount)?;
    // ...
}
```

Inbound bridging in `execute_vaa_v1.rs:307` remints through the issuance flow in `issue.rs:57`. That also does not trigger the transfer hook.

This means the bridge path applies lockup checks and destination-side issuance rules, but it never executes the source-chain transfer hook. The concrete gap is that same-investor cross-chain relocation is possible even when source-chain transfer-hook policies would block or limit a normal source-chain movement.

This is **not** an arbitrary-recipient or KYC bypass. The destination side still binds the transfer to the same investor: Solana inbound requires the recipient wallet to be linked to the payload investor's identity via `wallet_identity_account` and `identity_account` constraints in `execute_vaa_v1.rs:148` and `execute_vaa_v1.rs:166`, and the EVM side similarly requires the destination wallet to belong to the same investor.

**Impact:** If the intended security model is that transfer-hook restrictions also immobilize tokens against bridge exits, an investor can move value off the Solana Token-2022 mint through the bridge despite source-chain transfer-only policies. For example, a holder with sufficient unlocked balance can still bridge out while a `TransferPause`, `TransactionAmountLimit`, or `BlockFlowbackEndTime` policy is active, because those checks are not part of the bridge path. This weakens compliance and emergency-control assumptions around the source-chain asset, even though the tokens remain bound to the same investor on the destination chain.

**Recommended Mitigation:** If bridge exits are supposed to honor the same restrictions as ordinary transfers, add an explicit bridge validation path that mirrors the relevant source-chain transfer-hook policy checks before burning. The cleanest fix is to expose a dedicated policy-engine "validate bridge exit" interface and call it from `bridge_ds_tokens`.


**Securitize:** Acknowledged; We propose treating this as a known, intentional design property of DS Protocol.
