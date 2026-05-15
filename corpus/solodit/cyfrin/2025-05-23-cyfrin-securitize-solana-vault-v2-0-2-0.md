---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: Off-By-One Error in Liquidator and Operator Capacity Check
vuln_class: []
---

# Off-By-One Error in Liquidator and Operator Capacity Check

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** When adding new liquidators or operators, the check is performed to check that the MAX_LENGTH is greater than or equal the current length. But after this we push the new element.

> - bc-solana-vault-sc/programs/sc-vault/src/instructions/admin/add_liquidator.rs
>- bc-solana-vault-sc/programs/sc-vault/src/instructions/admin/add_operator.rs
```rust
pub fn add_liquidator_handler(
    ctx: &mut Context<AddLiquidator>,
    new_liquidator: Pubkey,
) -> Result<()> {
    let vault_state = &mut ctx.accounts.vault_state;

>>  require_gte!(
        MAX_LIQUIDATORS,
        vault_state.liquidators.len(),
        ScVaultError::MaxLiquidators
    );
    ...
>>  vault_state.liquidators.push(new_liquidator);
    ...
}
// ----------------
pub fn add_operator_handler(ctx: &mut Context<AddOperator>, new_operator: Pubkey) -> Result<()> {
    let vault_state = &mut ctx.accounts.vault_state;

>>  require_gte!(
        MAX_OPERATORS,
        vault_state.operators.len(),
        ScVaultError::MaxOperators
    );
    ...
>>  vault_state.operators.push(new_operator);
    ...
}
```

If the current length is the same as `MAX_LIQUIDATORS/OPERATORS` the check will pass, as it enforces the MAX to be greater than or equal. But this is incorrect. as if the length is the `MAX` we should prevent adding, as this will result in out of bound array access.

**Impact:** Incorrect behavior of the Program and getting incorrect error results.

**Recommended Mitigation:** Consider using `require_gt` instead of `require_gte`.

**Securitize:** Fixed in [179f8f3](https://github.com/securitize-io/bc-solana-vault-sc/commit/179f8f337b886edb1631c31537f62efb7ac8c47a).

**Cyfrin:** Verified
