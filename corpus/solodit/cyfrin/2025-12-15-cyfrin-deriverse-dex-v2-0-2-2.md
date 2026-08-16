---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Account Count Validation Mismatch in `new_base_crncy` Instruction
vuln_class: []
---

# Account Count Validation Mismatch in `new_base_crncy` Instruction

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `new_base_crncy` instruction has an inconsistency between the declared minimum account count and the actual number of accounts required.

The function comment and implementation both indicate that `9` accounts are needed, but `NewBaseCrncyInstruction::MIN_ACCOUNTS` is set to `8`.

```rust
pub fn new_base_crncy(program_id: &Pubkey, accounts: &[AccountInfo], _: &[u8]) -> DeriverseResult {
    // New Base Currency Instruction
    // 1 - Admin (Signer)
    // 2 - Root Account (Read Only)
    // 3 - Token Account
    // 4 - Program Token Account (Signer when creating a new token)
    // 5 - Deriverse Authority Account (Read Only)
    // 6 - Token Program ID (Read Only)
    // 7 - Mint Address (Read Only, when wSOL can not be old native mint)
    // 8 - System Program (Read Only)
    // 9 - Community Account
```

The function first reads 8 accounts, then later reads the 9th account:

```rust:145:src/program/processor/new_base_crncy.rs
    let community_acc = next_account_info!(accounts_iter)?;
```


However, the validation check only requires 8 accounts:

```rust:50-55:src/program/processor/new_base_crncy.rs
    if accounts.len() < NewBaseCrncyInstruction::MIN_ACCOUNTS {
        bail!(InvalidAccountsNumber {
            expected: NewBaseCrncyInstruction::MIN_ACCOUNTS,
            actual: accounts.len(),
        });
    }
```

Where `MIN_ACCOUNTS` is defined as:

```rust:281-285:constants.rs
    pub struct NewBaseCrncyInstruction;
    impl DrvInstruction for NewBaseCrncyInstruction {
        const INSTRUCTION_NUMBER: u8 = 4;
        const MIN_ACCOUNTS: usize = 8;
    }
```

**Impact:**
1. **Incorrect Validation**: The instruction accepts `8` accounts when it actually requires `9,` creating a mismatch between the validation and the actual account requirements.
2. **Late Failure**: Transactions with only `8` accounts will pass the initial check but fail later during execution.

**Recommended Mitigation:** Update `MIN_ACCOUNTS` to `9` to match the actual account requirements:

```rust
pub struct NewBaseCrncyInstruction;
impl DrvInstruction for NewBaseCrncyInstruction {
    const INSTRUCTION_NUMBER: u8 = 4;
    const MIN_ACCOUNTS: usize = 9;  // Changed from 8 to 9
}
```

**Deriverse:** Fixed in commit [f54117b0](https://github.com/deriverse/protocol-v1/commit/f54117b09012e11e0003844f5f855e6f878d3f73).

**Cyfrin:** Verified.
