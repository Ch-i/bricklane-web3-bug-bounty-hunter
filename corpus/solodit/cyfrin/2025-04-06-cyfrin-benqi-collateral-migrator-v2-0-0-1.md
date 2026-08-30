---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-06-cyfrin-benqi-collateral-migrator-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-06-cyfrin-benqi-collateral-migrator-v2-0
title: Migrating collateral will leave dust amounts of source tokens behind
vuln_class: []
---

# Migrating collateral will leave dust amounts of source tokens behind

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md)_

---

**Description:** When migrating collateral, the user provides two separate amounts related to how much of the source market tokens should be migrated: `migrationAmount` and `swapParams.fromAssetAmount`.

- `migrationAmount` is the number of `qiTokens` (Compound V2 `CTokens`) to redeem. This is handled in [`CollateralMigrator::LBFlashLoanCallback#L474-L482`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/CollateralMigrator.sol#L474-L482):

```solidity
// Redeem the migration amount from the source market
if (migrationAmount == type(uint256).max) {
    // Get the QiToken balance of the source market
    migrationAmount = IMinimalQiToken(sourceMarket).balanceOf(user);
}
// Transfer the QiTokens to the contract
IERC20(sourceMarket).safeTransferFrom(user, address(this), migrationAmount);
// Redeem the QiTokens from the source market
if (IMinimalQiToken(sourceMarket).redeem(migrationAmount) != 0) revert RedeemFailed();
```

- `swapParams.fromAssetAmount` is the amount of underlying source tokens to be swapped for target market tokens, as seen in [`CollateralMigrator::LBFlashLoanCallback#L490-L497`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/CollateralMigrator.sol#L490-L497):

```solidity
// Swap the underlying asset from the source market to the target market
_swap(
    _swapParams.fromAsset,
    _swapParams.toAsset,
    _swapParams.fromAssetAmount,
    _swapParams.minToAssetAmount,
    _swapParams.data
);
```

The issue lies in the mismatch between these values: `migrationAmount` represents a quantity of interest-bearing `qiTokens`, not the actual amount of underlying tokens they redeem for. Over time, `qiTokens` accumulate interest and represent a growing amount of the underlying asset.

Because the user must provide `fromAssetAmount` at the time of transaction submission, before the redemption happens, they must guess how much underlying they will receive. If they guess too high, the swap will revert. To avoid this, users are forced to guess conservatively and leave some underlying tokens unutilized in the `CollateralMigrator` contract.

**Impact:** Due to the interest-bearing nature of `qiTokens`, users cannot accurately determine how much underlying they will receive. As a result, dust amounts of leftover source tokens remain in the `CollateralMigrator` contract after the swap.

While these tokens are not permanently lost (they can be recovered via an admin-only `sweep` function), users are unable to fully migrate their position.

**Recommended Mitigation:** Consider removing the `fromAssetAmount` parameter entirely, as there's no known use case for performing a partial swap. Instead, swap the entire balance of the source asset:

```diff
  // Swap the underlying asset from the source market to the target market
  _swap(
      _swapParams.fromAsset,
      _swapParams.toAsset,
-     _swapParams.fromAssetAmount,
+     IERC20(_swapParams.fromAsset).balanceOf(address(this))
      _swapParams.minToAssetAmount,
      _swapParams.data
  );
```

**Benqi:** Fixed in commit [`e9525d1`](https://github.com/woof-software/benqi-collateral-migrator/commit/e9525d1676cf49fc59b513bbd3f37f41ef0bbe0c)

**Cyfrin:** Verified. Contract balance is now used as input amount to the swap.
