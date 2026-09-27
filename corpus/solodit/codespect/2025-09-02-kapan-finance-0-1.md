---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-0-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[H-02] Vesu Gateway uses the same default pool ID for every withdrawal'
vuln_class: []
---

# [H-02] Vesu Gateway uses the same default pool ID for every withdrawal

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`vesu_gateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/vesu_gateway.cairo#L147)

**Description:**

During withdrawals from Vesu, users specify from which pool they want to withdraw using the `context` field in the `Withdraw` struct:

```cairo
fn withdraw(ref self: ContractState, instruction: @Withdraw) {
    // ...
    if instruction.context.is_some() {
        let mut context_bytes: Span<felt252> = (*instruction.context).unwrap();
        let vesu_context: VesuContext = Serde::deserialize(ref context_bytes).unwrap();
        if vesu_context.pool_id != Zero::zero() {
            pool_id = vesu_context.pool_id;
        }
        if vesu_context.position_counterpart_token != Zero::zero() {
            debt_asset = vesu_context.position_counterpart_token;
        }
    }
    // ...
```

Later, contract needs to call the correct vToken address to convert user’s shares to assets. However, the vToken retrieved is not from the user’s specified `pool_id`:

```cairo
fn modify_collateral_for(
    ref self: ContractState,
    pool_id: felt252,
    collateral_asset: ContractAddress,
    debt_asset: ContractAddress,
    user: ContractAddress,
    collateral_amount: i257,
) -> UpdatePositionResponse {
    // ...
    // If this is negative, it means withdraw
    if collateral_amount.is_negative() {
        // @audit doesn't pass user's pool id
        let vtoken = self.get_vtoken_for_collateral(collateral_asset);

        let erc4626 = IERC4626Dispatcher { contract_address: vtoken };
        let requested_shares = erc4626.convert_to_shares(collateral_amount.abs());
        let available_shares = vesu_context.position.collateral_shares;
        assert(available_shares > 0, 'No-collateral');
        // ...
}
```

```cairo
fn get_vtoken_for_collateral(
    self: @ContractState, collateral: ContractAddress,
) -> ContractAddress {
    let vesu_singleton_dispatcher = ISingletonDispatcher {
        contract_address: self.vesu_singleton.read(),
    };
    // @audit uses contract's default pool id
    let poolId = self.pool_id.read();
    let extensionForPool = vesu_singleton_dispatcher.extension(poolId);
    let extension = IDefaultExtensionCLDispatcher { contract_address: extensionForPool };
    extension.v_token_for_collateral_asset(poolId, collateral)
}
```

As a result, the wrong vToken address is used to retrieve information about the user’s available shares and final withdraw amount.

**Impact:** Users are unable to withdraw from their required pools as the transaction will revert if they don’t have any shares in the default `pool_id`. Also, users who have shares in that pool will withdraw assets from that pool even if they specified another pool.

**Recommendation:** Pass users’ `pool_id` to the `get_vtoken_for_collateral(...)` function and use that to retrieve the extension contract address.

**Status:** Fixed
