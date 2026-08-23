---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Inconsistent Token Account Address Requirements Between Deposit and Withdraw
vuln_class: []
---

# Inconsistent Token Account Address Requirements Between Deposit and Withdraw

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `deposit()` and `withdraw()` functions have inconsistent requirements regarding token account addresses:

- **`deposit()`**: Allows deposits from any token account owned by the signer, not requiring an Associated Token Account (ATA)
- **`withdraw()`**: Requires withdrawals to go to the signer's ATA address only


**Deposit Function - No ATA Requirement:**

```rust
// deposit.rs lines 145-154
let old_token = check_spl_token(
    client_associated_token_acc,
    program_token_acc,
    token_state,
    token_program_id,
    mint,
    signer.key,  // Only verifies owner is signer
    &pda,
    data.token_id,
)?;
```

The `check_spl_token()` function (in `helper.rs`) only validates:
- Token account owner is the signer (line 207)
- Mint address matches
- Token program matches

```rust
        if client_token != *mint.key {
            bail!(InvalidMintAccount {
                token_id: token_state.id,
                expected_address: *mint.key,
                actual_address: client_token,
            });
        }

        let client_token_owner = client_token_acc.data.borrow()[32..].as_ptr() as *const Pubkey;

        if *client_token_owner != *signer {
            bail!(DeriverseErrorKind::InvalidTokenOwner {
                token_id: token_state.id,
                address: *client_token_acc.key,
                expected_adderss: *signer,
                actual_address: *client_token_owner,
            });
        }
```

**It does NOT verify the address is an ATA**, meaning users can deposit from any token account they control.

**Withdraw Function - ATA Required:**

```rust
// withdraw.rs lines 127-138
let expected_address = get_associated_token_address_with_program_id(
    signer.key,
    mint_acc.key,
    token_program_id.key,
);
if expected_address != *client_associated_token_acc.key {
    bail!(InvalidAssociatedTokenAddress {
        token_id: token_state.id,
        expected_address: expected_address,
        actual_address: *client_associated_token_acc.key,
    });
}
```

The `withdraw()` function explicitly requires the destination to be the signer's ATA address, rejecting any other token account address.

This works fine with Token-2022, as the owner of a token account is immutable. However, in the legacy token program, a user can transfer ownership of any token account. If a user who deposited funds no longer owns the associated token account, they will not be able to withdraw their funds using the withdraw function since we verify that the ATA owner must be the signer.

Here: https://github.com/solana-program/token/blob/main/program/src/processor.rs#L441

**Impact:** It can cause a loss of user funds. Here is the scenario:
1. The user had an ATA and transferred ownership of that ATA.
2. The user deposited using a different token account.
3. Since the user no longer owns the original ATA, and our logic checks that the ATA owner must match the user, any withdrawal attempt will fail. As a result, the user is unable to withdraw their funds.

**Recommended Mitigation:** Either:
- Make Both Functions Consistent (Require ATA/Allow Any Token Account)
- If the current asymmetry is intentional, clearly document why deposits allow flexibility and withdrawals require ATA.

**Deriverse:** Fixed in commit [1e3d88](https://github.com/deriverse/protocol-v1/commit/1e3d8857266eb82b1920b5edd09009041e96fafe).

**Cyfrin:** Verified.
