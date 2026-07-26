---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Inconsistent implementation approach for retrieving collateral balance from
  Morpho
vuln_class: []
---

# Inconsistent implementation approach for retrieving collateral balance from Morpho

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance::_collateralBalanceOfMorpho` uses direct storage slot access to retrieve a user's collateral balance from Morpho, while similar functionality for debt retrieval is implemented using `MorphoLib`. This inconsistency in the implementation approach makes the code less readable and maintainable.
```solidity
    function _collateralBalanceOfMorpho(
        Id morphoMarketId,
        address rockoWallet
    ) private view returns (uint256 totalCollateralAssets) {//@audit-issue use MorphoLib::collateral instead
        bytes32[] memory slots = new bytes32[](1);
        slots[0] = MorphoStorageLib.positionBorrowSharesAndCollateralSlot(morphoMarketId, rockoWallet);
        bytes32[] memory values = MORPHO.extSloads(slots);
        totalCollateralAssets = uint256(values[0] >> 128);
    }

    function _getMorphoDebtAndShares(Id marketId, address rockoWallet) private returns (uint256 debt, uint256 shares) {
        MarketParams memory marketParams = MORPHO.idToMarketParams(marketId);
        MORPHO.accrueInterest(marketParams);

        uint256 totalBorrowAssets = MORPHO.totalBorrowAssets(marketId);
        uint256 totalBorrowShares = MORPHO.totalBorrowShares(marketId);
        shares = MORPHO.borrowShares(marketId, rockoWallet);
        debt = shares.toAssetsUp(totalBorrowAssets, totalBorrowShares);
    }
```

**Recommended Mitigation:** Refactor `_collateralBalanceOfMorpho` to use `MorphoLib::collateral` for consistency with other parts of the codebase:

```diff
function _collateralBalanceOfMorpho(
    Id morphoMarketId,
    address rockoWallet
) private view returns (uint256 totalCollateralAssets) {
-    bytes32[] memory slots = new bytes32[](1);
-    slots[0] = MorphoStorageLib.positionBorrowSharesAndCollateralSlot(morphoMarketId, rockoWallet);
-    bytes32[] memory values = MORPHO.extSloads(slots);
-    totalCollateralAssets = uint256(values[0] >> 128);
+    totalCollateralAssets = MorphoLib.collateral(MORPHO, morphoMarketId, rockoWallet);
}
```

**Rocko:** Fixed in commit [5ef86b4](https://github.com/getrocko/onchain/commit/5ef86b44063a988afed93fe3f69074be757768bd).

**Cyfrin:** Verified.
