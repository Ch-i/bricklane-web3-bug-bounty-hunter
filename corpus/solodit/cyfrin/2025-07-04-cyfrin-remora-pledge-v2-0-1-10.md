---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Burning ALL PropertyTokens of a frozen holder results in the holder losing
  the payouts distribution while he was frozen
vuln_class: []
---

# Burning ALL PropertyTokens of a frozen holder results in the holder losing the payouts distribution while he was frozen

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Burning PropertyTokens from frozen holders has an edge case when all the tokens owned by a frozen holder get burned. This is how burning PropertyTokens impacts the payouts for distributions of frozen holders:
- If not all the PropertyTokens owned by a frozen holder are burned, the holder can still have access to the payouts for the distributions while he was frozen.
- If all the PropertyTokens owned by a frozen holder are burned, the holder would lose the payouts for the distributions while he was frozen.

The discrepancy in the behavior when burning PropertyTokens of Frozen Holders demonstrates an edge case that can result in frozen holders losing payouts.

For example - (Assume holders were frozen at the same index and got their tokens burned at the same index too):
- UserA has 1 PropertyToken and is frozen
- UserB has 2 PropertyTokens and is frozen too
- UserA and B get burned each a PropertyToken.
  - UserA loses the payouts distributions while he was frozen, whilst UserB still has access to the payouts for the 2 PropertyTokens that he owned during those distributions.

**Impact:** Burning ALL the PropertyTokens owned by a frozen holder causes the holder to lose the payouts for the distributions while he was frozen.

**Proof of Concept:** Run the following test to reproduce the issue described on the Description section
```solidity
    function test_frozenHolderLosesPayoutsBecauseItsTokensGotBurnt() public {
        address user1 = users[0];
        uint256 amountToMint = 2;

        // fund total payout amount to funding wallet
        uint64 payoutDistributionAmount = 100e6;

        // Distribute payouts for the first 5 distributions
        for(uint i = 1; i <= 5; i++) {
            _fundPayoutToPaymentSettler(payoutDistributionAmount);
        }

        _whitelistAndMintTokensToUser(user1, amountToMint);

        vm.prank(user1);
        remoraTokenProxy.approve(address(this), amountToMint);

        paySettlerProxy.initiateBurning(address(remoraTokenProxy), address(this), 0);

        // verify increased current payout index twice
        assertEq(remoraTokenProxy.getCurrentPayoutIndex(), 5);

        // Distribute payouts for distributions 5 - 10
        for(uint i = 1; i <= 5; i++) {
            _fundPayoutToPaymentSettler(payoutDistributionAmount);
        }

        // Freze user 2 at distributionIndex 10
        remoraTokenProxy.freezeHolder(user1);

        uint256 user1HolderBalanceAfterBeingFrozen = remoraTokenProxy.payoutBalance(user1);

        // Distribute payouts for distributions 10 - 15
        for(uint i = 1; i <= 5; i++) {
            _fundPayoutToPaymentSettler(payoutDistributionAmount);
        }

        // verify increased current payout index twice
        assertEq(remoraTokenProxy.getCurrentPayoutIndex(), 15);

        assertEq(user1HolderBalanceAfterBeingFrozen, remoraTokenProxy.payoutBalance(user1), "Frozen holder earned payout while being frozen");

        uint256 user1PayoutBalance = remoraTokenProxy.payoutBalance(user1);
        // 5 distributions of 100e6 all for user1
        assertEq(user1PayoutBalance, 500e6, "User1 Payout is incorrect");

        vm.prank(user1);
        remoraTokenProxy.claimPayout();
        assertEq(stableCoin.balanceOf(user1), user1PayoutBalance, "Error while claiming payout");
        assertEq(remoraTokenProxy.payoutBalance(user1), 0);

        //@audit-info => When the holder is unfrozen, he gets access to the payouts for al the distributions while he was frozen
        uint256 snapshotBeforeUnfreezing = vm.snapshotState();
        // unfreeze user1 and validate it gets access to all the distributions while it was frozen
        remoraTokenProxy.unFreezeHolder(user1);
        // After being unfrozen there were pending only 5 distributions of 100e6 all for user1
        assertEq(remoraTokenProxy.payoutBalance(user1), 500e6, "User1 Payout is incorrect");
        vm.revertToState(snapshotBeforeUnfreezing);

        uint256 snapshotBeforeBurningAllFrozenHolderTokens = vm.snapshotState();
        //@audit-info => Burning ALL PropertyTokens from a holder while is frozen results in the holder
        // NOT being able to access the payouts of the distributions while he was frozen
        remoraTokenProxy.burnFrom(user1, 2, false);
        assertEq(remoraTokenProxy.balanceOf(user1), 0);

        assertEq(remoraTokenProxy.payoutBalance(user1), 0);
        // unfreeze user1 and validate it loses the payouts of the distributions while it was frozen
        remoraTokenProxy.unFreezeHolder(user1);
        assertEq(remoraTokenProxy.payoutBalance(user1), 0);
        vm.revertToState(snapshotBeforeBurningAllFrozenHolderTokens);

        //@audit-info => Burning NOT ALL PropertyTokens from a holder while is frozen results in the holder
        // being able to access the payouts of the distributions while he was frozen
        assertEq(remoraTokenProxy.payoutBalance(user1), 0);
        remoraTokenProxy.burnFrom(user1, 1, false);
        assertEq(remoraTokenProxy.balanceOf(user1), 1);
        remoraTokenProxy.unFreezeHolder(user1);
        assertEq(remoraTokenProxy.payoutBalance(user1), 500e6);
    }
```

**Recommended Mitigation:** The least disruptive mitigation to prevent this issue is to add a check on the `burnFrom` to revert the tx if the account has been left without more propertyTokens and the account is frozen
```diff
function burnFrom(
        address account,
        uint256 value
    ) external restricted whenBurnable {
        _spendAllowance(account, _msgSender(), value);
        _burn(account, value);
+      if(balanceOf(account) == 0 && isHolderFrozen(account)) revert UserIsFrozen(account);
    }
```
Alternatively, similar to the burn(), revert if the account if frozen.
```diff
    function burnFrom(
        address account,
        uint256 value
    ) external restricted whenBurnable {
+       if (isHolderFrozen(account)) revert UserIsFrozen(account);
        _spendAllowance(account, _msgSender(), value);
        _burn(account, value);
    }
```

**Remora:** Fixed in commit [6008aec](https://github.com/remora-projects/remora-smart-contracts/commit/6008aecffdd83311e4552e8efee42eae59b3cd30) by preventing burning on frozen users.

**Cyfrin:** Verified.
