---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: deposit / withdraw round trip strands sub-wei dust in the vault and permanently
  inflates `assetDepositNet`
vuln_class: []
---

# deposit / withdraw round trip strands sub-wei dust in the vault and permanently inflates `assetDepositNet`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_T1e_Vault::withdrawERC20`, reached through the in-scope `STBL_XLayer_Asset_Vault` (which inherits `STBL_T1e_Vault`), computes the asset-side outflow as two separate floor-divided `fetchInversePrice` calls:

```solidity
uint256 withdrawAssetValue = iSTBL_Asset_Oracle(AssetData.oracle).fetchInversePrice(
    ((MetaData.stableValueNet + MetaData.haircutAmount) - withdrawfeeAmount)
);

uint256 withdrawFeeAssetValue = iSTBL_Asset_Oracle(AssetData.oracle).fetchInversePrice(
    withdrawfeeAmount
);
...
VaultData.assetDepositNet -= (withdrawAssetValue + withdrawFeeAssetValue);
```

`fetchInversePrice` is one floor division:

```solidity
inversePrice = (amount * (10 ** oracle.getPriceDecimals())) / oracle.fetchPrice();
```

The deposit path stores `MetaData.assetValue` directly into `VaultData.assetDepositNet` without any inversion. The two paths are asymmetric: deposit adds an exact `assetValue`, withdraw subtracts the sum of two floor-divisions of derived USD amounts. When the oracle price has a prime-fraction divisor (the harness's asset 1 uses `price = 1.12 * 10^18`), the floor truncation does not cancel between the two `fetchInversePrice` calls, and the round trip leaves a residue.

The residue is **not** credited to `VaultData.depositFees`, `withdrawFees`, `yieldFees`, or `insuranceFees`. It stays in the vault's token balance and `VaultData.assetDepositNet` retains the matching overcount, both growing linearly with every deposit / withdraw cycle.

**Impact:** Each deposit and withdraw cycle on an asset whose oracle price is not an integer factor of `10 ** priceDecimals` leaves one wei of asset token permanently stranded in the vault and overstates `assetDepositNet` by the same amount, inflating the yield differential consumed by `iDistributeYield`.

**Proof of Concept:** Five deposit/withdraw cycles on asset 1 (`price = 1.12 * 10^18`) and asset 2 (`price = 112 * 10^18`). Asset 1 drifts by one wei per cycle; asset 2 (integer divisor) does not drift.

```solidity
function test_FINDING_AccountingDust_Accumulates() public {
    uint256 amount = 1_000 * 10 ** 18;
    uint256 cycles = 5;
    for (uint256 i = 0; i < cycles; i++) {
        vm.warp(block.timestamp + 1 days);

        vm.prank(user1);
        uint256 lotId = xLayerWrapper.ess_deposit(amount);

        vm.warp(block.timestamp + 3 days);

        vm.startPrank(user1);
        xLayerToken.approve(address(xLayerWrapper), type(uint256).max);
        xLayerWrapper.ess_withdraw(lotId);
        vm.stopPrank();

        VaultStruct memory v1c = vault1.fetchVaultData();
        VaultStruct memory v2c = vault2.fetchVaultData();
        emit log_named_uint("v1.assetDepositNet", v1c.assetDepositNet);
        emit log_named_uint("v2.assetDepositNet", v2c.assetDepositNet);
        emit log_named_uint("vault1 token bal",
            testToken1.balanceOf(address(vault1)));
        emit log_named_uint("vault2 token bal",
            testToken2.balanceOf(address(vault2)));
    }
}
```

Output:

```text
cycle 1: v1.assetDepositNet = 1, vault1 balance = 1, v2 = 0, vault2 = 0
cycle 2: v1.assetDepositNet = 2, vault1 balance = 2, v2 = 0, vault2 = 0
cycle 3: v1.assetDepositNet = 3, vault1 balance = 3, v2 = 0, vault2 = 0
cycle 4: v1.assetDepositNet = 4, vault1 balance = 4, v2 = 0, vault2 = 0
cycle 5: v1.assetDepositNet = 5, vault1 balance = 5, v2 = 0, vault2 = 0
```

The drift is isolated to floor truncation inside `fetchInversePrice` on assets whose oracle price is not an integer factor of `10 ** priceDecimals`.


**Recommended Mitigation:** Symmetrize the deposit and withdraw paths so the floor errors cancel. The simplest fix is to derive the withdraw asset value from the deposit-time `MetaData.assetValue` rather than re-inverting `stableValueNet + haircutAmount`:

```solidity
uint256 withdrawFeeAssetValue = iSTBL_Asset_Oracle(AssetData.oracle)
    .fetchInversePrice(withdrawfeeAmount);

uint256 withdrawAssetValue = MetaData.assetValue - withdrawFeeAssetValue;
```

This matches the deposit accounting exactly. Alternatively, capture the rounding remainder explicitly (`MetaData.assetValue - withdrawAssetValue - withdrawFeeAssetValue`) and credit it to one of the fee buckets so it is recoverable through `iWithdrawFees` instead of stranded.

**STBL:** Acknowledged.

\clearpage
