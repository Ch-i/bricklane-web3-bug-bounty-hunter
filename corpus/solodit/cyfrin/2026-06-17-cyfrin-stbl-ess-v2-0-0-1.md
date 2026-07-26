---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_Redemption_Core::iDeposit` mints LP shares 1:1 instead of at the current
  pool rate, diluting new LPs into existing ones whenever the pool is off-peg'
vuln_class: []
---

# `STBL_Redemption_Core::iDeposit` mints LP shares 1:1 instead of at the current pool rate, diluting new LPs into existing ones whenever the pool is off-peg

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** The pool prices LP claims as a share-vault. `iFetchShare` (`contracts/redemption/STBL_Redemption_Core.sol:97-102`) values a user's claim as:

```solidity
return (userData[_user].stableValueNet * MetaData.stableValueNet) / totalSupply;
//      user_shares                     * pool_value                / total_shares
```

So `userData[user].stableValueNet` is a **share count**, not raw assets. For a share-vault to be fair, new shares must be minted at the current rate (`assets * totalSupply / poolValue`). `iDeposit` (`:121-135`) instead mints 1:1, ignoring the pool's per-share value:

```solidity
userData[msg.sender].stableValueNet += MetaData.stableValueNet;
totalSupply                          += MetaData.stableValueNet;
```

After any `redeem`, the pool NFT shrinks but `totalSupply` does not (`iRedeem`, `:172-202`), so per-share value drifts below 1. Every subsequent deposit then mints shares that are worth less than what the new LP paid in. The shortfall transfers pro-rata to the LPs already in the pool.

**Impact:** Once the pool is off-peg (`poolValue < totalSupply`), every new deposit is silently underwater. The new LP's booked shares equal what they deposited, but those shares price below par, so `iFetchShare` returns less than they paid. The missing value transfers, dollar-for-dollar, to existing LPs. The path is:

- Permissionless — any USST holder can drift the rate via `redeem`; any new LP then deposits.
- Atomic — dilution happens inside the deposit transaction, no opt-out.
- Repeatable — every deposit while off-peg is mispriced.
- Unrecoverable — no admin rebalance or sweep exists.

In the PoC: Charlie deposits ~$5,000 of `stableValueNet`, his immediate `iFetchShare` is only ~$3,667 (~27% loss in one tx), and the missing ~$1,333 lands on Alice with no action from her.

**Proof of Concept:** Add the following test to a file under `foundry_test/` whose contract extends `RedemptionTest`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Test.sol";
import "forge-std/console.sol";
import {RedemptionTest} from "./Redemption.t.sol";
import {STBL_TestToken} from "@stbl-protocol/stbl-contracts-evm-asset-type1/contracts/test/STBL_TestToken.sol";

contract PoC_DepositDilution is RedemptionTest {
    function test_PoC_iDepositDilutesNewLPs() public {
        // 1) Alice is the initial LP.
        uint256 aNft = _issueNFT(user1, DEPOSIT);
        uint256 aliceDeposited = yld.getNFTData(aNft).stableValueNet;
        vm.startPrank(user1);
        yld.approve(address(redemption), aNft);
        redemption.deposit(aNft);
        vm.stopPrank();
        _skipLockPeriod();

        // 2) Bob redeems — drives per-share value below 1.
        _issueNFT(user2, DEPOSIT);
        uint256 redeemAmt = (aliceDeposited * 6) / 10;
        vm.startPrank(user2);
        usst.approve(address(redemption), redeemAmt);
        redemption.redeem(redeemAmt);
        vm.stopPrank();

        uint256 poolBefore = yld.getNFTData(redemption.getNFTID()).stableValueNet;
        uint256 supplyBefore = redemption.getTotalSupply();
        assertLt(poolBefore, supplyBefore, "off-peg: poolValue < totalSupply");
        (uint256 aliceBooked, , ) = redemption.getUserData(user1);
        uint256 aliceClaimPre = (aliceBooked * poolBefore) / supplyBefore;

        // 3) Charlie deposits into the off-peg pool.
        address charlie = makeAddr("charlie");
        vm.prank(admin);
        STBL_TestToken(getAssetToken(ASSET_SLOT)).mint(charlie);
        uint256 cNft = _issueNFT(charlie, DEPOSIT / 2);
        uint256 charlieDeposited = yld.getNFTData(cNft).stableValueNet;
        vm.startPrank(charlie);
        yld.approve(address(redemption), cNft);
        redemption.deposit(cNft);
        vm.stopPrank();

        (uint256 charlieBooked, , ) = redemption.getUserData(charlie);
        uint256 poolAfter = yld.getNFTData(redemption.getNFTID()).stableValueNet;
        uint256 supplyAfter = redemption.getTotalSupply();
        uint256 charlieClaim = (charlieBooked * poolAfter) / supplyAfter;
        uint256 aliceClaimPost = (aliceBooked * poolAfter) / supplyAfter;

        console.log("per-share (1e18)   :", (poolBefore * 1e18) / supplyBefore);
        console.log("Charlie deposited  :", charlieDeposited);
        console.log("Charlie withdrawble:", charlieClaim);
        console.log("Charlie LOSS       :", charlieDeposited - charlieClaim);
        console.log("Alice GAIN         :", aliceClaimPost - aliceClaimPre);

        assertLt(charlieClaim, charlieDeposited, "Charlie diluted");
        assertGt(aliceClaimPost, aliceClaimPre, "Alice captured value");
        assertApproxEqAbs(
            aliceClaimPost - aliceClaimPre,
            charlieDeposited - charlieClaim,
            1e6,
            "loss transferred to Alice"
        );
    }
}
```

Run with:

```bash
forge test --match-contract PoC_DepositDilution -vv
```

Observed output (PASS):

```text
[PASS] test_PoC_iDepositDilutesNewLPs() (gas: 4475927)
Logs:
  per-share (1e18)   : 600000000000000000        (0.60, drifted from 1.00)
  Charlie deposited  : 4999999850000000000000    (~$5,000)
  Charlie withdrawble: 3666666556666666666666    (~$3,667)
  Charlie LOSS       : 1333333293333333333334    (~$1,333, 27%)
  Alice GAIN         : 1333333293333333333333    (== Charlie's loss)
```

**Recommended Mitigation:** Mint shares at the current pool exchange rate (the ERC-4626 `convertToShares` pattern):

```solidity
uint256 sharesToMint;
if (NFTID == 0) {
    sharesToMint = MetaData.stableValueNet;          // first-ever deposit: 1:1 is fine
    NFTID = _id;
} else {
    uint256 poolValue = YLD.getNFTData(NFTID).stableValueNet;
    sharesToMint = (MetaData.stableValueNet * totalSupply) / poolValue;
    NFTID = spliter.merge(NFTID, _id);
}
userData[msg.sender].stableValueNet += sharesToMint;
totalSupply                          += sharesToMint;
```

With this change, Charlie in the PoC receives ~`8.33e21` shares instead of `5e21`, and his immediate `iFetchShare` becomes exactly ~`5e21` — the dilution disappears.

Also consider pre-seeding `totalSupply` with a small "dead shares" amount at deployment (standard ERC-4626 first-depositor-attack mitigation), so the very first depositor can't be griefed by an attacker donating directly to the pool NFT to set an adversarial initial rate.

**STBL:** Fixed in commit [32f6d32](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/32f6d322a5fe3060ff8afd175d02bdcdc4592053).

**Cyfrin:** Verified. `iDeposit` now mints LP shares at the current pool exchange rate — `sharesToMint = (depositedValue * totalSupply) / poolValue` — instead of 1:1. This ensures that when the pool is off-peg (poolValue < totalSupply due to prior redemptions), a new depositor receives fewer shares that correctly reflect the pool's current backing, rather than receiving par shares that are immediately underwater and transferring the shortfall to existing LPs.

\clearpage
