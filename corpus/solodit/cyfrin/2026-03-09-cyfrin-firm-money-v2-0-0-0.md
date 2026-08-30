---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: Deployment script is missing new collaterals support
vuln_class: []
---

# Deployment script is missing new collaterals support

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** The `DeployLiquity2Script` defines `NUM_BRANCHES = 6` to support ETH, wstETH, rETH, SNT, LINEA, and sGUSD. However, the mainnet deployment path only handles the first three collaterals. Collateral token assignments, price feed deployments, and `TroveManagerParams` for the new branches are incomplete. A mainnet deployment would revert due to uninitialized collateral addresses, a failing `assert` in `_deployPriceFeed`, and the resulting zero-address entries being passed to `CollateralRegistry`.

**Impact:** Mainnet deployment will fail for branches 3-5 (SNT, LINEA, sGUSD). The `_deployPriceFeed` function hits `assert(_collTokenAddress == RETH_ADDRESS)` and reverts for any collateral beyond rETH. Even if bypassed, `CollateralRegistry` would be initialized with three `address(0)` collateral entries. Additionally, `TroveManagerParams` for the new collaterals are missing the `DEBT_LIMIT` field.

- Collateral assignments missing for indices 3–5:

https://github.com/firm-money/firm/blob/main/contracts/script/DeployLiquity2.s.sol#L654-L664

```solidity
if (block.chainid == 1 && !useTestnetPriceFeeds) {
  vars.collaterals[0] = IERC20Metadata(WETH);
  vars.collaterals[1] = IERC20Metadata(WSTETH_ADDRESS);
  vars.collaterals[2] = IERC20Metadata(RETH_ADDRESS);
  // @audit collaterals[3], [4], [5] never assigned for SNT, LINEA, sGUSD
}
```

- Zero-address collaterals passed to `CollateralRegistry`:

https://github.com/firm-money/firm/blob/main/contracts/script/DeployLiquity2.s.sol#L689

`r.collateralRegistry = new CollateralRegistry(r.boldToken, vars.collaterals, vars.troveManagers, deployer);`

`_deployPriceFeed` only handles three collaterals and reverts otherwise:

https://github.com/firm-money/firm/blob/main/contracts/script/DeployLiquity2.s.sol#L867-L901

```solidity
function _deployPriceFeed(address _collTokenAddress, address _borroweOperationsAddress)
  internal returns (IPriceFeed)
{
  if (block.chainid == 1 && !useTestnetPriceFeeds) {
      if (_collTokenAddress == address(WETH)) {
          return new WETHPriceFeed(...);
      } else if (_collTokenAddress == WSTETH_ADDRESS) {
          return new WSTETHPriceFeed(...);
      }
      // @audit reverts for SNT, LINEA, sGUSD
      assert(_collTokenAddress == RETH_ADDRESS);
      return new RETHPriceFeed(...);
  }
  return new PriceFeedTestnet();
}
```

- `TroveManagerParams` for new collaterals missing `DEBT_LIMIT`:

https://github.com/firm-money/firm/blob/main/contracts/script/DeployLiquity2.s.sol#L394-L421

```solidity
troveManagerParamsArray[3] = TroveManagerParams({
    CCR: CCR_SNT,
    MCR: MCR_SNT,
    SCR: SCR_SNT,
    BCR: BCR_ALL,
    LIQUIDATION_PENALTY_SP: LIQUIDATION_PENALTY_SP_SNT,
    LIQUIDATION_PENALTY_REDISTRIBUTION: LIQUIDATION_PENALTY_REDISTRIBUTION_SNT
    // @audit missing DEBT_LIMIT (same for indices 4 and 5)
});
```

**Recommended Mitigation:** Complete the mainnet deployment path: assign the three new collateral token addresses, add corresponding `else if` branches in `_deployPriceFeed` for `SNTPriceFeed`, `LINEAPriceFeed`, and `SGUSDPriceFeed`, and add the `DEBT_LIMIT` field to all three new `TroveManagerParams`.

**Firm Money:**
Fixed in commits [3a2e368](https://github.com/firm-money/firm/pull/16/changes/3a2e36855bb49c27cc5439a79ea49300942bc3a0), [59e4a8a](https://github.com/firm-money/firm/pull/21/changes/59e4a8ae721e269f2646aa71316b202d57ba7b49).

**Cyfrin:** Verified.
