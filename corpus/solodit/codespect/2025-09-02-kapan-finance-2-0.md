---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[L-01] Nostra positions are not getting tracked correctly'
vuln_class: []
---

# [L-01] Nostra positions are not getting tracked correctly

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`NostraGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/NostraGateway.cairo#L312)

**Description:**

In the Nostra protocol there are 2 types of collateral that users can have, Interest Bearing collateral and Non-Interest Bearing collateral. It is possible that users hold both of these debt tokens simultaneously. However, the `get_user_positions(...)` function doesn’t account for this scenario:

```cairo
fn get_user_positions(
    self: @ContractState, user: ContractAddress,
) -> Array<(ContractAddress, felt252, u256, u256)> {
    let mut positions = array![];
    let mut i = 0;
    while i != self.supported_assets.len() {
        let underlying = self.supported_assets.at(i).read();
        let symbol = IERC20SymbolDispatcher { contract_address: underlying }.symbol();

        let debt = self.underlying_to_ndebt.read(underlying);
        let collateral = self.underlying_to_ncollateral.read(underlying);
        let ibcollateral = self.underlying_to_nibcollateral.read(underlying);

        let debt_balance = IERC20Dispatcher { contract_address: debt }.balance_of(user);
        let collateral_raw = IERC20Dispatcher { contract_address: collateral }
            .balance_of(user);

        // @audit User can have collateral in both the collateral and ibcollateral tokens
        let collateral_balance = if collateral_raw == 0 {
            IERC20Dispatcher { contract_address: ibcollateral }.balance_of(user)
        } else {
            collateral_raw
        };
        positions.append((underlying, symbol, debt_balance, collateral_balance));
        i += 1;
    };
    return positions;
}
```

The function checks the user’s Non-Interest Bearing collateral balance and only if it’s 0 it checks for user’s Interest Bearing collateral balance.

**Impact:** The function always returns the balance of 1 type of collateral that the user holds and never the total of both of them. If a user is holding Non-Interest Bearing collateral tokens, his Interest Bearing collateral balance will not be accounted for.

**Recommendation:** Check for both of the balances and add them.

**Status:** Acknowledged

**Client response:** This one won’t be fixed in the release version as the UI does not support the nostra semantics. Users would be required to go through their portal to setup the tokens correctly for transfering debt for the time being.
