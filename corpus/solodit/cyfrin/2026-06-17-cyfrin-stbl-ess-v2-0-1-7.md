---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: accrued YieldDistributor rewards are permanently stranded once the asset leaves
  `ENABLED`, because `iClaim` is the only exit and it hard-reverts on any other status
vuln_class: []
---

# accrued YieldDistributor rewards are permanently stranded once the asset leaves `ENABLED`, because `iClaim` is the only exit and it hard-reverts on any other status

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** The YieldDistributor accumulates each NFT's pending reward in `stakingData[id].earned` and holds the corresponding token balance on its own address. The only path out is `iClaim`:

```solidity
function iClaim(uint256 id) internal virtual returns (uint256) {
    AssetDefinition memory AssetData = registry.fetchAssetData(assetID);
    if (!AssetData.isActive()) revert STBL_AssetDisabled(assetID);
    ...
    IERC20(AssetData.token).safeTransfer(YToken.ownerOf(id), reward);
    ...
}
```

`isActive()` is strict equality on `AssetStatus.ENABLED`. Both admin status-change paths (`disableAsset` → `DISABLED`, `emergenyStopAsset` → `EMERGENCY_STOP`) move status away from `ENABLED`, so every subsequent `claim` reverts. The YieldDistributor has no admin sweep, no force-claim, and no equivalent of `iEmergencyWithdraw`. The vault's own `iEmergencyWithdraw` sweeps only the vault's balance to the treasury and never touches the YieldDistributor:

```solidity
function iEmergencyWithdraw() internal virtual {
    ...
    uint256 balance = IERC20(AssetData.token).balanceOf(address(this));   // vault balance only
    IERC20(AssetData.token).safeTransfer(treasury, balance);
    ...
}
```

Tokens previously routed into the YieldDistributor via `distributeReward` therefore have no recovery path once the asset status changes. Each NFT's `stakingData[id].earned` becomes a write-only entry and the corresponding token balance is locked inside the YieldDistributor forever. `emergenyStopAsset` makes this permanent because the status is one-way; `disableAsset` blocks claims for the duration of the pause but the value is at least recoverable on re-enable.

A side effect of the same revert is that `STBL_UT1e_Issuer::iWithdraw` calls `yieldDistributor.claim` on the exit path, so `ess_withdraw` also reverts for lots touching a non-`ENABLED` asset. For `emergenyStopAsset` this is plausibly intentional — the protocol designs decommission as a one-way path with treasury-side compensation. The stranded yield is not justified by that design, because the yield is not part of the asset's principal that the treasury sweep is supposed to absorb.

The strand becomes outright permanent rather than merely awkward when combined with the vault's `EmergencyWithdraw` flow: the vault's swept balance lands at the treasury (so principal at least has an off-chain reconciliation surface), but the YieldDistributor's balance has no equivalent endpoint and no admin can route it anywhere from the moment status leaves `ENABLED`.

**Impact:** Once admin moves a basket asset to `EMERGENCY_STOP`, all token balance previously distributed to the YieldDistributor as user reward becomes permanently unrecoverable: NFT owners cannot claim it, the treasury sweep does not touch it, and there is no other extraction path.

**Proof of Concept:**
```solidity
function test_DisableAssetBricksWithdraw_ess() public {
    vm.prank(user1);
    uint256 lotId = xLayerWrapper.ess_deposit(DEPOSIT_AMOUNT);

    vm.warp(block.timestamp + 2 days);

    vm.prank(admin);
    registry.disableAsset(assetId1);

    // The same iClaim revert that strands the YieldDistributor's balance
    // also cascades up through iWithdraw and bricks ess_withdraw.
    vm.startPrank(user1);
    xLayerToken.approve(address(xLayerWrapper), type(uint256).max);
    vm.expectRevert();
    xLayerWrapper.ess_withdraw(lotId);
    vm.stopPrank();
}

function test_EmergencyStopBricksWithdraw_ess() public {
    vm.prank(user1);
    uint256 lotId = xLayerWrapper.ess_deposit(DEPOSIT_AMOUNT);

    vm.warp(block.timestamp + 2 days);

    vm.prank(admin);
    registry.emergenyStopAsset(assetId1);

    vm.startPrank(user1);
    xLayerToken.approve(address(xLayerWrapper), type(uint256).max);
    vm.expectRevert();
    xLayerWrapper.ess_withdraw(lotId);
    vm.stopPrank();
}
```

Both pass: claim reverts at `iClaim`, propagating up through `iWithdraw` to `ess_withdraw`. Once `emergenyStopAsset` makes the status change one-way, the corresponding YieldDistributor balance is permanently inaccessible.

**Recommended Mitigation:** Relax the `isActive()` precondition in `iClaim` so NFT owners retain the right to claim previously-accrued rewards regardless of the asset's lifecycle status. The claim only reads `stakingData[id].earned` and transfers from the YieldDistributor's own balance, so allowing it post-decommission does not violate any deposit-side invariant:

```solidity
function iClaim(uint256 id) internal virtual returns (uint256) {
    AssetDefinition memory AssetData = registry.fetchAssetData(assetID);
    // Claims of already-credited rewards remain permitted after decommission.
    ...
}
```

If the protocol explicitly wants claims gated on `ENABLED`, add a treasury-only sweep on the YieldDistributor under `EMERGENCY_STOP` so the value at least lands with the treasury alongside the vault sweep, rather than being permanently locked in the contract.

**STBL:** Fixed in commits [6a3df6e](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/6a3df6e5967e9c57a47cd2f0e2377186f3941df3#diff-04ac44f76e2124a33d4a9f41d18cb4226bc481ab0962daffd9a460ddeb5a4f78) && [37d5ee7](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/37d5ee7b9fea4f6824a72b2cb7160fdd3be319ea).

**Cyfrin:** Verified. The core-assets repo has been updated to allow claiming yield on disabled assets at this [commit](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-asset-type1/commit/923e46e9fa9f838d0529f3ef73e270f3c5baa0da).


\clearpage
