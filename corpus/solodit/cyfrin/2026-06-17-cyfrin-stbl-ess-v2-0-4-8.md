---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`withdrawERC20` charges the live registry `withdrawFee` instead of the deposit-time
  snapshot stored on the NFT'
vuln_class: []
---

# `withdrawERC20` charges the live registry `withdrawFee` instead of the deposit-time snapshot stored on the NFT

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** The issuer's `generateMetaData` explicitly snapshots six fee/duration fields onto the YLD NFT at deposit time, labelled `Snapshot of values`, and persists them as `MetaData.Fees` on the NFT:

```solidity
/** Snapshot of values */
MetaData.Fees.depositFee = AssetData.depositFees;
MetaData.Fees.withdrawFee = AssetData.withdrawFees;
MetaData.Fees.hairCut = AssetData.cut;
MetaData.Fees.insuranceFee = AssetData.insuranceFees;
MetaData.Fees.duration = AssetData.duration;
MetaData.Fees.yieldDuration = AssetData.yieldDuration;
```

Five of the six fields are consumed at the snapshotted value: `depositFee`, `hairCut`, `insuranceFee` feed deposit math via `MetaData.Fees.depositFee` etc., and `duration` and `yieldDuration` gate `iWithdraw`'s lock window via `MetaData.depositTimestamp + MetaData.Fees.duration` checks. The same persisted struct is what `getNFTData(id)` exposes externally, so any off-chain UI or aggregator reading the NFT will quote `Fees.withdrawFee` as the fee in force for that position.

`Fees.withdrawFee` is the single exception. `vault.withdrawERC20` ignores the persisted value and reads the live registry instead:

```solidity
uint256 withdrawfeeAmount = calculateWithdrawFees(
    MetaData,
    AssetData.withdrawFees   // live registry, not MetaData.Fees.withdrawFee
);
```

`STBL_Register::setFees` is callable at any time on any `ENABLED` asset with no timelock. `ess_withdraw` has no `maxFee` parameter or other slippage protection. Any `setFees` transaction landing between a deposit and a withdraw is enforced against the depositor at the new rate.

**Impact:** A `setFees` transaction landing between a depositor's commitment and their withdraw silently raises the fee on their already-snapshotted position with no caller-side opt-out, so a single fee update can apply the maximum allowed withdraw fee to every in-flight withdraw on the asset.

**Proof of Concept:** Depositors A and B both deposit identical baskets at `withdrawFee = 1%`. A withdraws under the original 1%, admin then raises the live registry fee to 50%, B withdraws expecting the 1% its NFTs snapshotted.

```solidity
function test_SnapshotIgnored_ChargesLiveFee() public {
    vm.prank(user_A);
    uint256 lotA = xLayerWrapper.ess_deposit(DEPOSIT_AMOUNT);

    vm.prank(user_B);
    uint256 lotB = xLayerWrapper.ess_deposit(DEPOSIT_AMOUNT);

    uint256[] memory idsB = xLayerNFTVault.fetchLotDetails(lotB).ids;
    assertEq(yld.getNFTData(idsB[0]).Fees.withdrawFee, FEE_AT_DEPOSIT);

    vm.warp(block.timestamp + 2 days);

    // A withdraws first, under the 1% live fee.
    vm.startPrank(user_A);
    xLayerToken.approve(address(xLayerWrapper), type(uint256).max);
    uint256 v1FeesBeforeA = vault1.fetchVaultData().withdrawFees;
    xLayerWrapper.ess_withdraw(lotA);
    uint256 v1FeesChargedA = vault1.fetchVaultData().withdrawFees - v1FeesBeforeA;
    vm.stopPrank();

    // Admin raises the live withdrawFee to 50%. NFT snapshots unchanged.
    vm.startPrank(admin);
    registry.setFees(assetId1, 0, FEE_RAISED, 0, 0);
    registry.setFees(assetId2, 0, FEE_RAISED, 0, 0);
    vm.stopPrank();

    assertEq(yld.getNFTData(idsB[0]).Fees.withdrawFee, FEE_AT_DEPOSIT);

    // B withdraws under the new 50% live fee.
    vm.startPrank(user_B);
    xLayerToken.approve(address(xLayerWrapper), type(uint256).max);
    uint256 v1FeesBeforeB = vault1.fetchVaultData().withdrawFees;
    xLayerWrapper.ess_withdraw(lotB);
    uint256 v1FeesChargedB = vault1.fetchVaultData().withdrawFees - v1FeesBeforeB;
    vm.stopPrank();

    // B paid ~50x A despite identical NFT snapshots.
    assertApproxEqRel(v1FeesChargedB, v1FeesChargedA * 50, 1e12);
}
```

Output:

```text
A asset1 withdraw fee charged: 2_678_571_428_571_428_571
B asset1 withdraw fee charged: 133_928_571_428_571_428_571
```

B paid ~50× A despite identical NFT snapshots.

**Recommended Mitigation:** Honour the snapshot the protocol already writes:

```solidity
uint256 withdrawfeeAmount = calculateWithdrawFees(
    MetaData,
    MetaData.Fees.withdrawFee
);
```

**STBL:** Acknowledged. By design, for the pegging system where deposit fees and withdrawal fees are directly tied to the pegging system.

\clearpage
