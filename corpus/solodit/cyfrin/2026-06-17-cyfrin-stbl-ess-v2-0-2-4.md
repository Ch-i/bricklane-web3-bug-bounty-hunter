---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_Redemption_Core::iClaimYield` floor-divides without a remainder carry,
  permanently stranding yield'
vuln_class: []
---

# `STBL_Redemption_Core::iClaimYield` floor-divides without a remainder carry, permanently stranding yield

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption_Core::iClaimYield` (`stbl-contracts-evm-redemptions/contracts/redemption/STBL_Redemption_Core.sol:113-119`) updates the reward index with a single floor division:

```solidity
rewardIndex += (_value * MULTIPLIER) / totalSupply;
```

`_value` is the asset-token amount the yield distributor transfers into the redemption contract (`STBL_T1_YieldDistributor::claim` at `stbl-contracts-evm-redemptions/.../STBL_T1_YieldDistributor.sol:235-255`: the distributor-side `earned` is reset to zero and the tokens are sent to `YToken.ownerOf(id)`, which is the redemption pool). LPs later claim against the index in `STBL_Redemption_Core::iClaim` (`stbl-contracts-evm-redemptions/contracts/redemption/STBL_Redemption_Core.sol:159-170`) via `_calculateRewards = shares * (rewardIndex - userIndex) / MULTIPLIER`.

Because the increment to `rewardIndex` is floor-divided, only `floor(_value * 1e18 / totalSupply) * totalSupply / 1e18` of the received tokens become claimable. The modulo (`_value` minus that) sits in the pool's asset balance forever. There is no `rewardRemainder` carry across calls and no sweep or reconciliation path anywhere in `STBL_Redemption` or `STBL_Redemption_Core`. The per-call strand is bounded by `totalSupply / 1e18` wei of asset token and accumulates monotonically across repeated calls.

**Impact:** Loss of funds, at dust scale under realistic parameters. The per-call strand is bounded by `totalSupply / 1e18`: microscopic for an 18-decimal asset at any normal pool size, but for a low-decimal high-supply pool the dust is non-trivial and accumulates over many years of repeated claims. It is unrecoverable because no sweep or admin path exists. Severity: Medium.

| `totalSupply` | per-call max strand (18-dec asset) | per-call max strand (6-dec asset) |
|---|---|---|
| `1e22` (10K stableValueNet) | `< 1e-14` token | `< 1e-2` USDC cent |
| `1e25` (10M stableValueNet) | `< 1e-11` token | `< 10` USDC cents |
| `1e28` (10B stableValueNet) | `< 1e-8` token | `< $10,000` USDC |

**Proof of Concept:** The following test lives in `stbl-contracts-evm-redemptions/foundry_test/PoC_Audit.t.sol` (contract `PoC_Audit` extends `RedemptionTest`):

```solidity
// iClaimYield strands remainder of (_value * 1e18) / totalSupply.
// The formula `rewardIndex += (_value * 1e18) / totalSupply` floor-divides.
// The remainder is not carried; it lives in the pool's asset balance forever.
function test_PoC_iClaimYieldStrandsRemainder() public {
    // 1) user1 deposits, becomes the sole LP.
    uint256 nft = _issueNFT(user1, DEPOSIT);
    vm.startPrank(user1);
    yld.approve(address(redemption), nft);
    redemption.deposit(nft);
    vm.stopPrank();

    // 2) Generate yield through the normal flow.
    _skipLockPeriod();
    vm.startPrank(admin);
    STBL_TestOracle(getAssetOracle(ASSET_SLOT)).setPrice();
    STBL_T1_Vault(getAssetVault(ASSET_SLOT)).distributeYield();
    vm.stopPrank();

    address assetToken = getAssetToken(ASSET_SLOT);
    uint256 balBefore = STBL_TestToken(assetToken).balanceOf(address(redemption));

    // 3) Pull yield from distributor into the pool.
    redemption.claimYield();
    uint256 balAfterClaimYield = STBL_TestToken(assetToken).balanceOf(address(redemption));
    uint256 valueReceived = balAfterClaimYield - balBefore;

    // 4) The sole LP claims. With totalSupply == userData[user1], user1 is
    //    entitled to 100% of the yield. Any residual after the LP has been
    //    paid is mathematically stranded.
    vm.prank(user1);
    uint256 lpReceived = redemption.claim();
    uint256 strandedInPool = STBL_TestToken(assetToken).balanceOf(address(redemption)) - balBefore;

    uint256 totalSupplyNow = redemption.getTotalSupply();
    uint256 strandThreshold = totalSupplyNow / 1e18; // bound on per-call strand

    console.log("totalSupply (shares)   :", totalSupplyNow);
    console.log("strand threshold (wei) :", strandThreshold);
    console.log("yield _value (wei)     :", valueReceived);
    console.log("LP received (wei)      :", lpReceived);
    console.log("stranded in pool (wei) :", strandedInPool);

    // Conservation: yield in == LP out + stranded.
    assertEq(lpReceived + strandedInPool, valueReceived, "conservation");
    // The sole LP owns 100% of the pool but cannot claim the full yield.
    assertLt(lpReceived, valueReceived, "LP cannot claim full yield");
    // Strand is bounded per-call but grows monotonically over repeated calls.
    assertGt(strandedInPool, 0, "remainder is stranded");
    assertLt(strandedInPool, strandThreshold, "bounded by totalSupply/1e18");
}
```

Run with `forge test --match-test test_PoC_iClaimYieldStrandsRemainder -vv`. Real output:

```text
[PASS] test_PoC_iClaimYieldStrandsRemainder() (gas: 1416409)
Logs:
  totalSupply (shares)   : 9999999700000000000000
  strand threshold (wei) : 9999
  yield _value (wei)     : 99009898019802000000
  LP received (wei)      : 99009898019801990297
  stranded in pool (wei) : 9703

Suite result: ok. 1 passed; 0 failed; 0 skipped
```

The sole LP, entitled to 100% of the pool, cannot claim the full yield: `9703 wei` is stranded and unrecoverable, bounded by `totalSupply / 1e18 = 9999 wei` as the formula predicts.

**Recommended Mitigation:** Carry the truncation remainder across calls:

```solidity
uint256 private rewardRemainder;

function iClaimYield() internal {
    if (totalSupply == 0) return;
    AssetDefinition memory AssetData = registry.fetchAssetData(AssetID);
    uint256 _value = iSTBL_YieldDistributor(AssetData.rewardDistributor).claim(NFTID);
    uint256 scaled  = _value * MULTIPLIER + rewardRemainder;
    rewardIndex    += scaled / totalSupply;
    rewardRemainder = scaled % totalSupply;
}
```

This preserves conservation across an arbitrary number of `claimYield` calls and eliminates the strand.

**STBL:** Fixed in commit [3c84f82](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/3c84f82a286ae4b69d39dbf8b7485a9ce2e08b12).

**Cyfrin:** Verified. `iClaimYield` function now carries the truncation remainder across calls via a new `rewardRemainder` state variable.
