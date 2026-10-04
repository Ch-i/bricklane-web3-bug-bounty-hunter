---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-02-cyfrin-atum-solana-v2-v2-0-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-04-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-02-cyfrin-atum-solana-v2-v2-0
title: Escrow ATA Balance Mismatch Enables Fee Bypass, Limit Bypass, and Accounting
  Inconsistency
vuln_class: []
---

# Escrow ATA Balance Mismatch Enables Fee Bypass, Limit Bypass, and Accounting Inconsistency

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-02-cyfrin-atum-solana-v2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-02-cyfrin-atum-solana-v2-v2.0.md)_

---

**Description:** Background: This behavior stems from the fix for **C-01** (donation-attack DOS on `close_account`). At the time of that fix, fees were not yet implemented, so using `escrow_ata.amount` as the gross and draining the entire balance was fully correct in the previous version of the codebase. The issue only surfaced after fees were introduced, which changed the assumptions under which the original fix was designed: the fee split now relies on a snapshotted `deposit.fee_amount` while the `gross` is dynamic, creating a mismatch.

The `release` instruction uses `ctx.accounts.escrow_ata.amount` (current ATA balance) as `gross` to prevent donation-attack DOS on close_account (C-01 fix in previous audit).

```rust
    // 3. Fee split calculation
    let gross = ctx.accounts.escrow_ata.amount;
    let fee = deposit.fee_amount;

    require!(gross >= fee, ErrorCode::InsufficientEscrowBalanceForFee);

    let net = gross.checked_sub(fee).unwrap();
```
At `deposit` time, the fee is computed and stored in `deposit.fee_amount`:

```rust
let fee_amount = compute_fee(
        amount,
        mint_decimals,
        mint_fee_config.fee_percentage_6,
        mint_fee_config.min_fee_6,
        mint_fee_config.max_fee_6,
    )?;
```

At release time, `gross` is taken from the current escrow ATA balance, while `fee` remains the snapshotted value:

```rust
// 3. Fee split calculation
    let gross = ctx.accounts.escrow_ata.amount;
    let fee = deposit.fee_amount;

    require!(gross >= fee, ErrorCode::InsufficientEscrowBalanceForFee);

    let net = gross.checked_sub(fee).unwrap();
```

However, there is no guarantee that the escrow ATA balance equals the original `deposit.amount`. Because SPL token accounts accept incoming transfers from anyone, the balance can be altered before release.

- Attack Scenario 1: Same User (Depositor) Donation

1. Depositor creates a deposit of 100 tokens. Fee is computed as 5 (5%), stored in `deposit.fee_amount`. `remaining_capacity` and `max_transfer_size` are enforced (e.g., max 100).
2. Before release, the depositor sends 50 additional tokens directly to the escrow ATA via a normal SPL transfer.
3. On release: `gross = 150`, `fee = 5`, `net = 145`.
4. Recipient receives 145; treasury receives 5.

Leading to:

- **Fee bypass:** Effective fee rate = 5/150 ≈ 3.33% instead of 5%. Protocol revenue is diluted.
- **Limit bypass:** `max_transfer_size` and `remaining_capacity` were enforced only at deposit. The effective payment is 150, exceeding the intended limits.
- **Payment flexibility:** The depositor can change the payment amount at any time before release by donating more tokens.

- Attack Scenario 2: Third-Party Donation (Grief / Inconsistency)

1. User A deposits 100 tokens for a recipient. Off-chain payment system expects recipient to receive `net = 95` (100 − 5 fee).
2. User B (or any address) sends 1 token to the escrow ATA.
3. On release: `gross = 101`, `fee = 5`, `net = 96`.
4. Recipient receives 96 instead of the expected 95.

Leading to:

- **Accounting inconsistency:** Off-chain systems that track expected amounts will mismatch on-chain results. Integrations that assume `net == deposit.amount - deposit.fee_amount` will break.

**Impact:**
1. **Protocol revenue loss:** Depositors can reduce effective fee rate by donating extra tokens.
2. **Invariant violation:** `max_transfer_size` and `remaining_capacity` can be circumvented.
3. **Integration risk:** Off-chain systems that assume deterministic `net` from `deposit.amount` and `deposit.fee_amount` will see incorrect amounts.
4. **Unpredictable payments:** Payment amount can be changed by anyone before release, undermining predictability for recipients and integrators.

**Recommended Mitigation:**
- Store the `fee_rate` and apply it during actual release on `gross`.
- And add intended `deposit.amount`  into the `Released` event.

**Atum:** Fixed in [b4c128e](https://github.com/Atum-Labs/solana-escrow/commit/b4c128e78d8b91112a242b652cfb8b8f4ee0e736).

**Cyfrin:** Verified.

\clearpage
