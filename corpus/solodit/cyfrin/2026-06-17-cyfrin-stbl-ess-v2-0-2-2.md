---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: 'Sole or last LP can never fully close their position and full-value redeem
  reverts: `split` rejects `_splitAssetValue >= stableValueNet`'
vuln_class: []
---

# Sole or last LP can never fully close their position and full-value redeem reverts: `split` rejects `_splitAssetValue >= stableValueNet`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `iWithdraw` routes every withdrawal through `spliter.split(NFTID, _amt)` (`contracts/redemption/STBL_Redemption_Core.sol:154`), and `iRedeem` routes every redemption through `spliter.split(NFTID, _amt)` (`contracts/redemption/STBL_Redemption_Core.sol:192`) after only requiring `MetaData.stableValueNet >= _amt` (`contracts/redemption/STBL_Redemption_Core.sol:176`). `STBL_YLD_SplitMerge::split` reverts with `STBL_InvalidSplitValue` whenever `_splitAssetValue >= meta.stableValueNet` (`contracts/splitter/STBL_YLD_SplitMerge.sol:105`). For the sole LP, `iFetchShare` returns the whole pooled value so `_amt == poolSVN == meta.stableValueNet`, and `split` reverts. A redeemer redeeming the full pooled value (`_amt == poolSVN`, allowed by the non-strict `>=` at line 176) hits the same revert.

**Impact:** The documented full-exit API is broken: a sole / last LP calling `withdraw(theirFullShare)` reverts, and any redeemer attempting `redeem(poolSVN)` reverts. Neither caller has a way to fully close the position - the contract has no non-`split` code path for the full-value case. The only workaround is to call with `_amt < poolSVN`, which always leaves a non-zero residual share on the LP (or residual pool NFT in the redeem case) that can never subsequently be redeemed, because every later attempt hits the same boundary. The LP can never **completely** close their position; the protocol carries a permanent stranded LP share with no recovery path.

**Proof of Concept:** Add the following tests to a file under `foundry_test/` whose contract extends `RedemptionTest` (provides `yld`, `redemption`, `usst`, `user1`, `user2`, `DEPOSIT`, `_issueNFT`, `_skipLockPeriod`):

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Test.sol";
import {RedemptionTest} from "./Redemption.t.sol";

contract PoC_SoleLpCannotExit is RedemptionTest {
    function test_PoC_SoleLpFullWithdrawReverts() public {
        uint256 nft1 = _issueNFT(user1, DEPOSIT);
        uint256 poolSVN = yld.getNFTData(nft1).stableValueNet;

        vm.startPrank(user1);
        yld.approve(address(redemption), nft1);
        redemption.deposit(nft1);
        vm.stopPrank();
        _skipLockPeriod();

        // require(iFetchShare >= _amt) passes (equality holds for sole LP),
        // but split(NFTID, poolSVN) reverts at _splitAssetValue >= meta.stableValueNet.
        vm.prank(user1);
        vm.expectRevert(); // STBL_InvalidSplitValue(poolSVN, poolSVN)
        redemption.withdraw(poolSVN);
    }

    function test_PoC_FullValueRedeemReverts() public {
        uint256 nft1 = _issueNFT(user1, DEPOSIT);
        uint256 poolSVN = yld.getNFTData(nft1).stableValueNet;

        vm.startPrank(user1);
        yld.approve(address(redemption), nft1);
        redemption.deposit(nft1);
        vm.stopPrank();
        _skipLockPeriod();

        // iRedeem's `MetaData.stableValueNet >= _amt` (non-strict) passes for
        // _amt == poolSVN, but split inside iRedeem then reverts.
        _issueNFT(user2, DEPOSIT); // user2 obtains USST
        vm.startPrank(user2);
        usst.approve(address(redemption), poolSVN);
        vm.expectRevert(); // STBL_InvalidSplitValue(poolSVN, poolSVN)
        redemption.redeem(poolSVN);
        vm.stopPrank();
    }
}
```

Run with:

```bash
forge test --match-contract PoC_SoleLpCannotExit -vv
```

Observed output (both PASS):

```text
[PASS] test_PoC_SoleLpFullWithdrawReverts() (gas: 1153260)
    -> withdraw(poolSVN) reverts at split's _splitAssetValue >= meta.stableValueNet
[PASS] test_PoC_FullValueRedeemReverts() (gas: 1889074)
    -> redeem(poolSVN) reverts at the same split boundary
```

Reasoning: for the sole LP, `iFetchShare == poolSVN == meta.stableValueNet`, so `_amt == meta.stableValueNet` and `split` reverts with `STBL_InvalidSplitValue`. Same boundary fires for `redeem(poolSVN)` because the iRedeem `require` is non-strict (`>=`) but `split` is strict (`>=` rejects equality).

**Recommended Mitigation:** Handle the full-value case without calling `split`. When `_amt == meta.stableValueNet`, transfer/withdraw the pooled `NFTID` directly (no split) instead of routing through `spliter.split`:

```solidity
if (_amt == MetaData.stableValueNet) {
    // full exit: hand over / burn NFTID directly, no split
} else {
    (uint256 _A, uint256 _B) = spliter.split(NFTID, _amt);
    ...
}
```

**STBL:** Fixed in commit [0d350da](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/0d350dab99839d6dcea00076c2796b822cbaf436).

**Cyfrin:** Verified. Blocking a 100% exit is intended so the pool never resets to empty. `iRedeem` reverts when `stableValueNet - buffer < _amt`, keeping at least `buffer` in the pool, and `split` keeps the strict `_splitAssetValue < stableValueNet` bound so the last LP withdraws down to a 1 wei residual. The leftover is dust, not a stranded position.
