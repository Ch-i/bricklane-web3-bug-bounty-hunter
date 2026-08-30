---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_Redemption_Core::iRedeem` burns the wrong split slice, causing an internal
  amount mismatch and DoS-ing `redeem` for `_amt < poolSVN/2`'
vuln_class: []
---

# `STBL_Redemption_Core::iRedeem` burns the wrong split slice, causing an internal amount mismatch and DoS-ing `redeem` for `_amt < poolSVN/2`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `iRedeem` (`contracts/redemption/STBL_Redemption_Core.sol:172-202`) is internally inconsistent about which value should be burned. `split(NFTID, _amt)` returns `_A` worth `_amt` and `_B` worth `poolSVN - _amt`, but the function keeps `_A` as the new pool and sends `_B` to `issuer.withdraw`:

```solidity
(uint256 _A, uint256 _B) = spliter.split(NFTID, _amt);
NFTID = _A;
// ...
iSTBL_Issuer(AssetData.issuer).withdraw(_B);
```

At the same time, it only collects/approves `_amt` USST from the redeemer:

```solidity
IERC20(registry.fetchUSSTToken()).transferFrom(msg.sender, address(this), _amt);
IERC20(registry.fetchUSSTToken()).approve(registry.fetchUSSTToken(), _amt);
```

In the PT1 flow, `withdraw(_B)` leads to `core.exit(..., _B, MetaData.stableValueNet)` and then `USST.burn(..., _value)` where `_value == _B.stableValueNet == poolSVN - _amt`.

So the function burns based on `poolSVN - _amt` while collecting only `_amt`. Whenever `poolSVN - _amt > _amt` (equivalently `_amt < poolSVN/2`), `safeTransferFrom` reverts with `ERC20InsufficientAllowance`. The PT1 PoC demonstrates this concretely; any issuer path that burns via `core.exit` with the same amount coupling inherits the same mismatch.

**Impact:** `redeem(_amt)` deterministically reverts for every input in `(0, poolSVN/2)` due to the internal amount mismatch. For `_amt` in `[poolSVN/2, poolSVN)`, calls can pass but the user pays `_amt` USST while redemption is priced off `poolSVN - _amt`, which is economically unfavorable. No attacker setup is required; the function self-fails from its own arithmetic.

**Proof of Concept:** Add the following test to a file under `foundry_test/` whose contract extends `RedemptionTest`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Test.sol";
import {RedemptionTest} from "./Redemption.t.sol";

contract PoC_RedeemAllowanceDoS is RedemptionTest {
    function test_PoC_SmallRedeemRevertsOnAllowance() public {
        // user1 funds the pool.
        uint256 nft1 = _issueNFT(user1, DEPOSIT);
        uint256 poolSVN = yld.getNFTData(nft1).stableValueNet;
        vm.startPrank(user1);
        yld.approve(address(redemption), nft1);
        redemption.deposit(nft1);
        vm.stopPrank();
        _skipLockPeriod();

        // user2 obtains USST and attempts an economically-rational redeem.
        _issueNFT(user2, DEPOSIT);
        uint256 redeemAmt = 1e18; // tiny vs poolSVN (~1e22), well under poolSVN/2
        assertLt(redeemAmt, poolSVN / 2, "rational range");

        vm.startPrank(user2);
        usst.approve(address(redemption), redeemAmt);
        // ERC20InsufficientAllowance(USST, 1e18, ~poolSVN) - issuer needs
        // _B.stableValueNet allowance (= poolSVN - _amt), iRedeem only approved _amt.
        vm.expectRevert();
        redemption.redeem(redeemAmt);
        vm.stopPrank();
    }
}
```

Run with:

```bash
forge test --match-test test_PoC_SmallRedeemRevertsOnAllowance -vv
```

Observed output (PASS):

```text
[PASS] test_PoC_SmallRedeemRevertsOnAllowance() (gas: 3136558)
    -> redeem(1e18) reverts with ERC20InsufficientAllowance(USST, 1e18, ~9.998e21)
```

**Recommended Mitigation:** Align the burned slice with the user input amount. The slice passed to `withdraw` should be the `_amt` slice, and the pool should retain the remainder. Derive USST approval from the same burned-slice metadata to keep the burn amount and allowance consistent.

In `split(NFTID, _amt)`, `_A` is the `_amt` slice and `_B` is the remainder.

Suggested change in `iRedeem`:

```diff
(uint256 _A, uint256 _B) = spliter.split(NFTID, _amt);
// before:
-NFTID = _A;
-IERC20(registry.fetchUSSTToken()).approve(registry.fetchUSSTToken(), _amt);
-iSTBL_Issuer(AssetData.issuer).withdraw(_B);

// after:
+NFTID = _B; // pool keeps the remainder
+YLD_Metadata memory burnedMeta = YLD.getNFTData(_A);
+IERC20(registry.fetchUSSTToken()).approve(
+    registry.fetchUSSTToken(),
+    burnedMeta.stableValueNet
+);
+iSTBL_Issuer(AssetData.issuer).withdraw(_A);
```

After the burn, reset the allowance to zero (or use `forceApprove` / `safeIncreaseAllowance` plus a matching reset).

**STBL:** Fixed in commit [f6a7fe7](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/f6a7fe7a75b1e298a10ac5ca82192514ca5ac382).

**Cyfrin:** Verified. `iRedeem` now correctly assigns the split slices — the pool retains `_B` (the remainder) as the new `NFTID` and passes `_A` (worth exactly `_amt`) to `issuer::withdraw`. This aligns the burned slice with the `_amt` of `USST` collected from the redeemer, eliminating the `allowance` mismatch that caused all redemptions below `poolSVN/2` to revert unconditionally.
