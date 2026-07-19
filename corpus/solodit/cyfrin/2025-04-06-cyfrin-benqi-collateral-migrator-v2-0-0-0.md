---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-06-cyfrin-benqi-collateral-migrator-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-06-cyfrin-benqi-collateral-migrator-v2-0
title: '`CollateralMigrator` reverts when pre-existing funds are used for flash loan
  fees'
vuln_class: []
---

# `CollateralMigrator` reverts when pre-existing funds are used for flash loan fees

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md)_

---

**Description:** The flow for migrating collateral between two markets is as follows:

1. The end user calls `CollateralMigrator::migrateCollateral` with the required swap parameters.
2. `CollateralMigrator` takes a flash loan from a Trader Joe liquidity pair.
3. Using the flash loan, `CollateralMigrator` opens a position in the target market.
4. With the position now overcollateralized, the original source market position can be closed.
5. The source tokens are swapped for target tokens.
6. The target tokens are used to repay the flash loan along with associated fees.
7. Any remaining target tokens are deposited into the target market on behalf of the user.

The `CollateralMigrator` contract is not intended to retain any funds after execution. However, if tokens remain in the contract (e.g., from a previous failed transaction), a user might attempt to use those to partially cover the flash loan fees.

This approach would cause a revert in [`CollateralMigrator::LBFlashLoanCallback`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/CollateralMigrator.sol#L488-L511):

```solidity
uint256 contractBalanceBF = IERC20(trgMarketConfig.flashData.baseToken).balanceOf(address(this));

// Swap the underlying asset from the source market to the target market
_swap(
    ...
);

// Return the flash loaned amount to the liquidity book pair
uint256 flashAmountWithFee = flashAmount +
    (trgMarketConfig.flashData.isTokenX ? totalFees.decodeX() : totalFees.decodeY());

// IEIP20NonStandard(flashData.baseToken).transfer(address(flashData.liquidityBookPair), flashAmountWithFee);
IERC20(trgMarketConfig.flashData.baseToken).safeTransfer(
    address(trgMarketConfig.flashData.liquidityBookPair),
    flashAmountWithFee
);

// Return the remaining underlying asset to the market
uint256 contractBalanceAF = IERC20(trgMarketConfig.flashData.baseToken).balanceOf(address(this));
// @audit if existing funds were used to pay fees, this will underflow
uint256 remainingAmount = contractBalanceAF - contractBalanceAF - contractBalanceBF;
```

If any pre-existing funds are used to pay the flash loan fees, the line `contractBalanceAF - contractBalanceBF` will underflow, since `contractBalanceAF` will be lower than `contractBalanceBF`.

**Impact:** Using pre-existing tokens in the contract to cover flash loan fees will cause the transaction to revert due to an underflow.

**Proof of Concept:** Add the following test to `CollateralMigrator.test.ts`, under `context("Migration functions")`:
```javascript
it("Migrate will not work when existing balance is used for fees", async function () {
    const { user, collateralMigrator, swapRouter, qiUSDT, qiDAI, USDT, DAI, usdtDaiLBPair } = await loadFixture(setupEnv);

    const fromMarket = qiUSDT.address;
    const toMarket = qiDAI.address;

    const fromAsset = USDT.address;
    const toAsset = DAI.address;
    const migrationAmount = parseEther("200");

    await usdtDaiLBPair.connect(user).setFeeBps(1000); // 10%

    await USDT.connect(user).mint(user.address, migrationAmount);
    await DAI.connect(user).mint(collateralMigrator.address, parseEther("20"));

    // we simulate that we need the amount of a flash loan for all 100% of the position (exchange rate 1:1)
    const flashAmount = parseEther("200");

    const data = swapRouter.interface.encodeFunctionData("swap", [
        fromAsset,
        toAsset,
        parseEther("200"),
        parseEther("200")
    ]);

    const swapParams = {
        fromAsset,
        toAsset,
        fromAssetAmount: parseEther("200"),
        minToAssetAmount: parseEther("200"),
        data: data
    };

    // approve the collateral migrator to spend the collateral
    await USDT.connect(user).approve(qiUSDT.address, MaxUint256);
    await qiUSDT.connect(user).mint(migrationAmount);

    await qiUSDT.connect(user).approve(collateralMigrator.address, migrationAmount);

    await expect(
        collateralMigrator
            .connect(user)
            .migrateCollateral(fromMarket, toMarket, migrationAmount, flashAmount, swapParams)
        ).to.be.reverted; // revert on underflow
});
```
Note: this also requires the following changes to `contracts/mocks/MockLBPair.sol` to support fees:
```diff
diff --git a/contracts/mocks/MockLBPair.sol b/contracts/mocks/MockLBPair.sol
index 6074fa2..a1d28bd 100644
--- a/contracts/mocks/MockLBPair.sol
+++ b/contracts/mocks/MockLBPair.sol
@@ -16,6 +16,8 @@ contract MockLBPair {
     uint16 private _binStep;
     address private _factory;

+    uint128 feeBps;
+
     constructor(address tokenX, address tokenY, uint16 binStep, address factory) {
         _tokenX = tokenX;
         _tokenY = tokenY;
@@ -42,15 +44,21 @@ contract MockLBPair {
     function flashLoan(ILBFlashLoanCallback receiver, bytes32 amounts, bytes calldata data) external {
         (uint amountX, uint amountY) = amounts.decode();

+        bytes32 fees;
+
         if (amountX > 0 && amountY == 0) {
             IERC20(_tokenX).transfer(address(receiver), amountX);
+            uint128 feeX = uint128(amountX) * feeBps / 10000;
+            fees = feeX.encode(0);
         } else if (amountX == 0 && amountY > 0) {
             IERC20(_tokenY).transfer(address(receiver), amountY);
+            uint128 feeY = uint128(amountY) * feeBps / 10000;
+            fees = uint128(0).encode(feeY);
         } else {
             revert("MockLBPair: INVALID_AMOUNTS");
         }

-        receiver.LBFlashLoanCallback(msg.sender, _tokenX, _tokenY, amounts, 0, data);
+        receiver.LBFlashLoanCallback(msg.sender, _tokenX, _tokenY, amounts, fees, data);
     }

     function encodeAmounts(uint128 amountX, uint128 amountY) external pure returns (bytes32) {
@@ -86,4 +94,8 @@ contract MockLBPair {
     function getFactory() external view returns (address factory) {
         return _factory;
     }
+
+    function setFeeBps(uint128 _feeBps) external {
+        feeBps = _feeBps;
+    }
 }
```

**Recommended Mitigation:** Instead of calculating the difference between the pre- and post-swap balances, consider refunding the entire remaining balance directly:

```diff
- uint256 contractBalanceBF = IERC20(trgMarketConfig.flashData.baseToken).balanceOf(address(this));

  ...

  // Return the remaining underlying asset to the market
- uint256 contractBalanceAF = IERC20(trgMarketConfig.flashData.baseToken).balanceOf(address(this));
- uint256 remainingAmount = contractBalanceAF - contractBalanceAF - contractBalanceBF;
+ uint256 remainingAmount = IERC20(trgMarketConfig.flashData.baseToken).balanceOf(address(this));

  if (remainingAmount > 0) {
      _supplyToMarket(user, targetMarket, remainingAmount);
  }
```

**Benqi:** Fixed in commit [`3828ee7`](https://github.com/woof-software/benqi-collateral-migrator/commit/3828ee73ac4471d58824b2f6051a3a8049b9cadc)

**Cyfrin:** Verified. Ingoing balance is now tracked. If the swap doesn't leave enough balance to cover the flashloan and fees execution will revert.
