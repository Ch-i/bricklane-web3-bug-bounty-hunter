---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: Dead Error Variants and Documentation Inconsistency for Signature Requirements
vuln_class: []
---

# Dead Error Variants and Documentation Inconsistency for Signature Requirements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** The error variants `VaultSignatureRequired` and `InvestorSignatureRequired` are defined in `errors.rs` but never used in the program logic. Additionally, the README references `require_investor_and_vault_signatures` and states that "both the investor and vault keypairs must sign," whereas the actual state field is `require_investor_signature` and vault signature is never enforced, creating documentation inconsistency.


In `programs/vault-registrar/src/errors.rs`:

```rust
#[msg("Vault signature required: vault wallet must sign the transaction")]
VaultSignatureRequired,

#[msg("Investor signature required: existing_investor_wallet must sign the transaction")]
InvestorSignatureRequired,
```

In `register_vault`, when `require_investor_signature` is true, only `InvestorAccountsRequired` is used:

```rust
if vault_registrar_state.require_investor_signature {
    require!(
        ctx.accounts.existing_investor_wallet.is_some()
            && ctx.accounts.existing_investor_wallet_identity.is_some(),
        VaultRegistrarError::InvestorAccountsRequired
    );
}
```

`VaultSignatureRequired` and `InvestorSignatureRequired` are never referenced in the program, so they are dead code.

Also,
> When `require_investor_and_vault_signatures` is true, pass `investorKp` and `existingInvestorWalletIdentity`:

> When `require_investor_and_vault_signatures` is true on the registrar, both the investor and vault keypairs must sign the transaction. Use `--investor-wallet-path` and `--vault-keypair-path` in that case.

The actual state field is `require_investor_signature` (singular), and `vault_wallet` is an `UncheckedAccount`—the program never enforces vault signature. Only the investor signature is enforced indirectly via `existing_investor_wallet: Option<Signer<'info>>` when the account is provided.

**Impact:**
- **Dead code**: Increases maintenance burden and may mislead future developers into believing vault signature verification exists.
- **Documentation mismatch**: The incorrect field name and the claim that "both" must sign can cause integration errors or incorrect expectations.

**Recommended Mitigation:** **Remove unused error variants** and **Fix README** if needed.

**Securitize:** Fixed in [2251615](https://github.com/securitize-io/bc-solana-whitelister/commit/2251615f8b553fd0c78685332eeb8164536ff939).

**Cyfrin:** Verified.
