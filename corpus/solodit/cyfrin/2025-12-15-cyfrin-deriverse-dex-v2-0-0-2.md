---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: 'Airdrop Implementation Issues: Unvalidated Ratio and Potential Transfer Direction
  Mismatch'
vuln_class: []
---

# Airdrop Implementation Issues: Unvalidated Ratio and Potential Transfer Direction Mismatch

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `airdrop` function is intended to convert user-earned `points` into DRVS tokens. However, the implementation has the following issues:

**Issue 1: Unvalidated Ratio Parameter**

The `AirdopOnChain` trait implementation only validates data format, not the `ratio` value:

```rust
impl AirdopOnChain for AirdropData {
    fn new(instruction_data: &[u8]) -> Result<&Self, DeriverseError> {
        bytemuck::try_from_bytes::<Self>(instruction_data)
            .map_err(|_| drv_err!(InvalidClientDataFormat))  // Only format check
    }
}
```

The `ratio` is then used directly without any bounds checking:

```rust
amount = ((amount as f64) * data.ratio) as u64;  // No validation on ratio!
```

This allows users to set `ratio` to arbitrary values (e.g., `1,000,000.0`, etc.), this could lead to token supply inflation or other calculation errors.

**Issue 2: Potential Transfer Direction Mismatch (Requires Team Confirmation)**


The current implementation transfers tokens FROM the user(`drvs_client_associated_token_acc`) to the program(`drvs_program_token_acc`):

```rust
let transfer_to_taker_ix = spl_token_2022::instruction::transfer_checked(
    &spl_token_2022::id(),
    drvs_client_associated_token_acc.key,  // FROM: User's account
    drvs_mint.key,
    drvs_program_token_acc.key,            // TO: Program's account
    signer.key,                            // Authority: User
    &[signer.key],
    amount,
    decs_count as u8,
)?;

invoke(
    &transfer_to_taker_ix,
    &[
        token_program.clone(),
        drvs_client_associated_token_acc.clone(),  // User account (source)
        drvs_mint.clone(),
        drvs_program_token_acc.clone(),            // Program account (destination)
        signer.clone(),                            // User signature
    ],
)?;
```

This is inconsistent with:
- The function name "airdrop" which typically implies sending tokens to users
- The expected behavior where users get rewarded for their accumulated points

Normally, the protocol should
- either directly transfer tokens to the user
- or mint tokens to the user,
- or mint them and immediately deposit them, followed by updating the client state with `client_state.add_asset_tokens(amount as i64)?;.`

Given that, this issue still requires the team's confirmation.

**Impact:**
- With unvalidated `ratio`, users could set extremely large values (e.g., `1,000,000.0`)
- The implementation could be inconsistent with the initial design, causing loss for the users.

**Recommended Mitigation:**
1. If `ratio` should be protocol-controlled, remove it from instruction data and calculate it based on protocol state.
2. If the `Potential Transfer Direction Mismatch` is confirmed, it is recommended to replace the transfer logic. If it's not a bug, the function name and documentation should be updated to reflect this behavior clearly.

**deriverse:**
Fixed in commit [f03ba7](https://github.com/deriverse/protocol-v1/commit/f03ba71ca5c0fcbc481a84e0487381f40f8985ed).

**Cyfrin:** Verified.
