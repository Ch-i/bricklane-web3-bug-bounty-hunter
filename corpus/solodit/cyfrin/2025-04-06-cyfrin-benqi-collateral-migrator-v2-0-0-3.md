---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-06-cyfrin-benqi-collateral-migrator-v2-0-0-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-06-cyfrin-benqi-collateral-migrator-v2-0
title: Unbounded loop in `CollateralMigrator::_removeMigrationConfigData` may hinder
  contract maintainability
vuln_class: []
---

# Unbounded loop in `CollateralMigrator::_removeMigrationConfigData` may hinder contract maintainability

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md)_

---

**Description:** [`CollateralMigrator::_removeMigrationConfigData`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/CollateralMigrator.sol#L790-L827)  contains an unbounded loop when removing migration configurations:
```solidity
function _removeMigrationConfigData(address market) private {
    uint32 length = uint32(_markets.length);
    bool found = false;

    for (uint256 i = 0; i < length; i++) {
        if (_markets[i] == market) {
            found = true;
            // remove the market from the list
            _markets[i] = _markets[length - 1];
            _markets.pop();

            // remove the market data and flash data
            delete _migrationConfigData[market];

            emit MigrationConfigDataRemoved(market);
            break;
        }
    }
    // revert if the market is not found
    if (!found) revert MarketIsNotSupported(market);
}
```
This implementation uses a linear search to find the market to remove. If a large number of markets are added, the loop may consume excessive gas, especially for markets positioned near the end of the array. In the worst-case scenario, the transaction could exceed the block gas limit, making it impossible to remove a market.

Additionally, removing markets located near the end of the array incurs higher gas costs, which may become non-trivial as the list grows.

**Impact:** In the worst case, removing a market could fail due to running out of gas. Even when successful, removals, especially of markets toward the end of the list, can become unnecessarily expensive.

**Recommended Mitigation:** Consider changing the function to accept the index of the market to remove rather than performing a linear search. This would eliminate the unbounded loop and reduce gas usage:

```solidity
function _removeMigrationConfigData(uint256 index) external onlyRole(DEFAULT_ADMIN_ROLE) {
    address market = _markets[index];

    _markets[index] = _markets[_markets.length - 1];
    _markets.pop();

    delete _migrationConfigData[market];

    emit MigrationConfigDataRemoved(market);
}
```

**Benqi:** Fixed in commit [`64aba7b`](https://github.com/woof-software/benqi-collateral-migrator/commit/64aba7b71a824e6ac20ae07c8f7746d785e425e0)

**Cyfrin:** Verified. A mapping `_marketIndex` was added to track markets to indexes. This is used to call `_removeMigrationConfigData` and the loop is removed.

\clearpage
