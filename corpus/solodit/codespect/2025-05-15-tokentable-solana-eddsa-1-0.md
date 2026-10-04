---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-05-15-tokentable-solana-eddsa-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-05-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md
tags:
- firm:codespect
- report:2025-05-15-tokentable-solana-eddsa
title: '[I-01] Changing the projectToken might not be functional.'
vuln_class: []
---

# [I-01] Changing the projectToken might not be functional.

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-05-15-TokenTable-Solana-EDDSA.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-05-15-TokenTable-Solana-EDDSA.md)_

---

**Files:** [set_base_params.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-distributor-solana/src/instructions/set_base_params.rs#L16), [deposit.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/87b79fe77b74d734fc5274da93300aa39444146c/programs/eddsa-token-distributor-solana/src/instructions/deposit.rs#L50)

**Description:**

In the `set_base_params` instruction, the airdrop owner is allowed to modify the token account used for the airdrop.

```rust
pub fn set_base_params(
    ctx: Context<SetBaseParams>,
    _project_id: String,
    token: Pubkey,
    start_time: u64,
    end_time: u64,
    authorized_signer: Pubkey
) -> Result<()> {
    //...
    ctx.accounts.airdrop.token = token;
```

However, switching may not function properly because the vault associated with the airdrop is singular and may have already been initialized as a `TokenAccount` for the previous mint. Moreover, the vault initialization lacks permission control, and the initializer is not required to hold the corresponding token.

```rust
pub struct Deposit<'info> {
    //...
    pub airdrop: Account<'info, Airdrop>,
    #[account(
        init_if_needed,
        payer = authority,
        seeds = [b"vault".as_ref(), airdrop.key().as_ref()],
        bump,
        token::mint = token_mint,
        token::authority = airdrop,
        token::token_program = token_program
    )]
    pub vault: InterfaceAccount<'info, TokenAccount>,
```

**Impact:** Modifying the token associated with the airdrop account may not be feasible. For instance:

1. The project initializes the airdrop account, and the token is set to `mint1`;
2. Another user calls `deposit`, which initializes the vault as a `TokenAccount` for `mint1`;
3. The project then calls `set_base_params` to change the token to `mint2`;
4. When the project tries to deposit `mint2` tokens, it fails because the vault was already initialized as a `TokenAccount` for `mint1` by another user;

**Recommendation(s):** It is recommended to add permission control to the `deposit` instruction, allowing only the airdrop owner to call it.

**Status:** Fixed

**Update from TokenTable:** Removed the ability to update the project token using `set_base_params()` in all affected programs in [a30590bd697e7564447b3e0e48e64199f06fea7e](https://github.com/EthSign/tokentable-unlocker-solana/commit/a30590bd697e7564447b3e0e48e64199f06fea7e).
