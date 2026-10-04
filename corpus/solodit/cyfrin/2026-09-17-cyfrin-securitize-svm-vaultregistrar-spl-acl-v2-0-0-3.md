---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-0-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: An investor can pre-attach a predictable DS vault and block its Registrar registration
vuln_class: []
---

# An investor can pre-attach a predictable DS vault and block its Registrar registration

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** Note: DS only. This is found during the path comparison between DS and SPL token.

The bug is who creates `WalletIdentity` first. Identity Registry owns a unique PDA `WalletIdentity(wallet, mint)` and `init`s it. Vault Registrar, rwa-rbac, and rwa-imr all write that same account. The registrar assumes an existing record is a prior registration. An investor can create it earlier through IMR, without going through the registrar at all. SPL registration uses whitelist `InvestorRegistry` and does not have this path.

A registrar instance is created with `initialize`, for one mint. It stores `admin`, `asset_mint`, and `operators` (max 10). The instance cannot register DS vaults until the DS token admin assigns RWA RBAC user role id to the **registrar state PDA**. That grant is outside `initialize`.

[`programs/vault-registrar/src/instructions/admin/initialize.rs`](https://github.com/securitize-io/bc-solana-whitelister/blob/main/programs/vault-registrar/src/instructions/admin/initialize.rs#L28-L96) · [`docs/VAULT_REGISTRAR_GUIDE.md` §6.1](https://github.com/securitize-io/bc-solana-whitelister/blob/main/docs/VAULT_REGISTRAR_GUIDE.md)

```
vault_registrar program
  └── VaultRegistrarState  (PDA ["vault_registrar_state", id], one mint)
        ├── admin
        ├── operators          ← DeFi protocols that may call register_vault_ds
        └── asset_mint
```

Two different “roles”:

- Registrar **operator**: a key that is allowed to call `register_vault_ds`.
- RBAC **user role id 1** on the **state PDA**: what lets that PDA pass `ATTACH_WALLET_TO_IDENTITY` when it CPIs into rwa-rbac.


1. Normal registration

Protocol (operator) → Vault Registrar → rwa-rbac → Identity Registry.

Demo passes its singleton vault PDA into the registrar:

[`programs/demo_defi_protocol/src/instructions/register_vault_ds.rs`](https://github.com/securitize-io/bc-solana-whitelister/blob/main/programs/demo_defi_protocol/src/instructions/register_vault_ds.rs#L73-L111)

That vault address is `PDA(["vault"], BhPDdnSU41tVqCChVSkLqdzJgmh3vr9ER7U1b39oWwzX)`. Program id and seed are public, so the address is known before `demo_defi_protocol::initialize` creates the account:

[`programs/demo_defi_protocol/src/lib.rs`](https://github.com/securitize-io/bc-solana-whitelister/blob/main/programs/demo_defi_protocol/src/lib.rs#L9-L20) · [`initialize.rs`](https://github.com/securitize-io/bc-solana-whitelister/blob/main/programs/demo_defi_protocol/src/instructions/initialize.rs#L5-L25)

```rust
declare_id!("BhPDdnSU41tVqCChVSkLqdzJgmh3vr9ER7U1b39oWwzX");

#[account(
    init,
    payer = payer,
    space = 8 + VaultState::INIT_SPACE,
    seeds = [b"vault"],
    bump
)]
pub vault: Account<'info, VaultState>,
```

Registrar checks pause + authorized caller, derives the same `WalletIdentity` PDA, and attaches only if it is still empty:

[`programs/vault-registrar/src/instructions/register_vault_ds.rs`](https://github.com/securitize-io/bc-solana-whitelister/blob/main/programs/vault-registrar/src/instructions/register_vault_ds.rs#L18-L179)

```rust
constraint = !vault_registrar_state.paused,
constraint = vault_registrar_state.is_authorized_caller(&caller.key()),

let (expected_vault_wallet_identity, _) = Pubkey::find_program_address(
    &[
        ctx.accounts.vault_wallet.key().as_ref(),
        ctx.accounts.asset_mint.key().as_ref(),
    ],
    ctx.accounts.identity_registry_program.key,
);

if !vault_wallet_identity_info.data_is_empty() {
    // same identity → VaultAlreadyRegistered
    // other identity → VaultBelongsToDifferentInvestor
}

rwa_rbac::cpi::attach_wallet_to_identity(
    /* user = vault_registrar_state, signed with registrar seeds */,
    cpi_data,
)?;
```

First hop: the **state PDA** signs as `user`. rwa-rbac checks `ATTACH_WALLET_TO_IDENTITY` on that PDA. This is why the role must already have been granted.

Second hop: rwa-rbac signs as **`controller_authority`** with `controller_seeds` (`[controller.key, bump]`) and CPIs into Identity Registry. That PDA is `identity_registry.authority`.

[`programs/rwa-rbac/.../attach_wallet_to_identity.rs`](https://github.com/securitize-io/rwa-rbac/blob/main/programs/rwa-rbac/src/instructions/cpi/identity_registry/attach_wallet_to_identity.rs#L38-L73)

```
Protocol operator
  → register_vault_ds
      → rwa-rbac attach (user = VaultRegistrarState, role already granted)
          → Identity Registry attach (authority = controller_authority)
              → init WalletIdentity
```

Documented CPI depth: Protocol → VaultRegistrar → rwa-rbac → Identity Registry. [`docs/INTEGRATION_GUIDE_DS.md`](https://github.com/securitize-io/bc-solana-whitelister/blob/main/docs/INTEGRATION_GUIDE_DS.md#L407-L418)

Identity Registry then `init`s `WalletIdentity(wallet, mint)`:

```rust
#[account(
    init,
    seeds = [wallet.key().as_ref(), asset_mint.key().as_ref()],
    payer = payer,
    space = 8 + WalletIdentity::INIT_SPACE,
    bump,
)]
pub wallet_identity: Box<Account<'info, WalletIdentity>>;
```

That `init` is first-writer-wins. The authority Identity Registry actually checks is not only the controller. It accepts either `identity_registry.authority` (the controller path above) **or** `identity_account.owner` (the investor PDA):

```rust
require!(
    ctx.accounts.authority.key() == ctx.accounts.identity_account.owner
        || ctx.accounts.authority.key() == ctx.accounts.identity_registry.authority,
    IdentityRegistryErrors::UnauthorizedSigner
);
```

[`programs/identity_registry/.../attach_wallet_to_identity.rs`](https://github.com/tiago18c/rwa-token/blob/main/programs/identity_registry/src/instructions/account/attach_wallet_to_identity.rs#L5-L55)



2. What a normal investor can do

They never touch the registrar. A registered investor calls IMR `attach_wallet_by_investor` and passes the predictable vault address as `new_wallet`. Public entrypoint: [`programs/rwa-imr/src/lib.rs`](https://github.com/securitize-io/rwa-rbac/blob/main/programs/rwa-imr/src/lib.rs#L43-L48)

The caller must already be an investor on that mint and must sign with a wallet already attached to their identity. Random keys cannot do this:

[`programs/rwa-imr/.../attach_wallet_by_investor.rs`](https://github.com/securitize-io/rwa-rbac/blob/main/programs/rwa-imr/src/instructions/attach_wallet_by_investor.rs#L12-L52)

```rust
pub wallet: Signer<'info>,
/// CHECK: For wallet to be added. Verified in CPI
pub new_wallet_identity: UncheckedAccount<'info>,

pub fn handler(ctx: Context<AttachWalletByInvestor>, new_wallet: Pubkey) -> Result<()> {
    let wallet_identity = WalletIdentity::deserialize_checked(&ctx.accounts.wallet_identity)?;
    require_keys_eq!(wallet_identity.identity_account, ctx.accounts.identity_account.key());
    require_keys_eq!(ctx.accounts.wallet.key(), wallet_identity.wallet);
```

`new_wallet` is only an instruction argument. The target does not sign, does not need to exist, and may be another program’s PDA:

```rust
let mut cpi_data = ATTACH_WALLET_TO_IDENTITY_IX.to_vec();
cpi_data.extend(new_wallet.as_ref());

AccountMeta::new_readonly(ctx.accounts.investor.key(), true), // investor PDA = identity_account.owner
invoke_signed(/* Identity Registry attach */, signers_seeds)?;
```

[Same file L42–L99](https://github.com/securitize-io/rwa-rbac/blob/main/programs/rwa-imr/src/instructions/attach_wallet_by_investor.rs#L42-L99)

This transaction never enters Vault Registrar, so pause, operator, and `require_investor_signature` are all skipped. Identity Registry accepts IMR’s investor-PDA signature as `identity_account.owner` — the left-hand branch. No RBAC role, no `controller_seeds`.

If `WalletIdentity` is already initialized, IR `init` fails. The race is to land before the legitimate `register_vault_ds`.


When the operator later registers, the registrar sees a non-empty account: wrong identity → `VaultBelongsToDifferentInvestor`; same identity → `VaultAlreadyRegistered`. It does not CPI attach and does not emit `VaultRegisteredDs`.

[Registrar L122–L132](https://github.com/securitize-io/bc-solana-whitelister/blob/main/programs/vault-registrar/src/instructions/register_vault_ds.rs#L122-L132) · tests for those two errors (after a successful registrar write, same branch): [spec L934–L990](https://github.com/securitize-io/bc-solana-whitelister/blob/main/tests/specs/vault-registrar.spec.ts#L934-L990)

```
Investor (already registered, signs an attached wallet)
  → IMR attach_wallet_by_investor(new_wallet = vault PDA)
      → Identity Registry attach (authority = investor PDA)
          → init WalletIdentity  ← occupies the account the registrar needed
```

Note: For SPL path, a freeze authority or whitelist admin *can* pre-create the registry. But that is a privileged write they already have.

**Impact:** If the vault address is predictable — as in the demo, `PDA(["vault"])` — any other registered investor can occupy it. Investor B attaches that address to B’s own identity through IMR before the protocol registers it for investor A. `register_vault_ds` then returns `VaultBelongsToDifferentInvestor`, so A cannot onboard the protocol.

That is the poison: the `WalletIdentity` slot for the vault is taken. B does not get the vault’s key or its tokens; A just cannot complete registration on that address.

Note: For SPL path, a freeze authority or whitelist admin *can* pre-create the registry. But that is a privileged write they already have.

**Recommended Mitigation:** Either:

1. On `attach_wallet_by_investor`, require proof of control of `new_wallet` (the wallet signs, or the owning program CPI-signs for a PDA). Do not accept an unauthenticated pubkey.
2. Document that a predictable vault address can be bound by another investor before registrar onboarding. Treat those cases as an operational/compliance issue: watch for them and Perform some actions on the malicious address.


**Securitize:** Acknowledged and documented in commit [c16281c](https://github.com/securitize-io/bc-solana-whitelister/commit/c16281cdbaa481df52942facca776b1a637aaa59).
