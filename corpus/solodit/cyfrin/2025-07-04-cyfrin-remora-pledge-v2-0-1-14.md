---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-14
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`RemoraToken` transfers are bricked when `from` is not whitelisted, has sufficient
  tokens to transfer but no tokens locked'
vuln_class: []
---

# `RemoraToken` transfers are bricked when `from` is not whitelisted, has sufficient tokens to transfer but no tokens locked

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `RemoraToken::adminTransferFrom`, `transfer` and `transferFrom` always check if `from` is on the whitelist and if not, call `_unlockTokens`:
```solidity
    bool fromWL = whitelist[from];
    bool toWL = whitelist[to];

    if (!fromWL) _unlockTokens(from, value, false);
    if (!toWL) _lockTokens(to, value);
```

But a scenario can occur where:
1) `from` has nothing to unlock
2) `from` has tokens to fulfill the transfer

In this case transfer would be bricked. Another scenario to consider is when:

1) `from` has 10 tokens
2) only 5 of those tokens are locked
3) `from` is attempting to transfer 10 tokens

In this case the call to `_unlockTokens` should have `amount = 5` since `from` only needs to unlock 5 tokens in order to send the 10 total.

But with the current code the call to `_unlockTokens` will have `amount = 10` (since it just uses the transfer amount) which makes no sense and causes a revert.

**Impact:** `RemoraToken` transfers are bricked when `from` is not whitelisted, has sufficient tokens to transfer but no tokens locked since the call to `_unlockTokens` will revert.

**Proof Of Concept:**
```solidity
function test_transferBricked_fromNotWhitelisted_ButHasTokensToTransfer() external {
    address from = users[0];
    address to = users[1];
    uint256 amountToTransfer = 1;

    // fund `from` with remora tokens
    remoraTokenProxy.mint(from, amountToTransfer);
    assertEq(remoraTokenProxy.balanceOf(from), amountToTransfer);

    // remove `from` from whitelist
    remoraTokenProxy.removeFromWhitelist(from);

    // set lock time
    remoraTokenProxy.setLockUpTime(3600);

    vm.expectRevert(); // reverts with InsufficientTokensUnlockable
    vm.prank(from);
    remoraTokenProxy.transfer(to, amountToTransfer);
}
```

This also totally bricks transfers for users who received tokens when they were whitelisted, then are removed from the whitelist:
```solidity
    function test_transferBricked_whitelistedHolderIsRemovedFromWhitelist() external {
        address from = users[0];
        address to = users[1];
        uint256 amountToTransfer = 10;

        _whitelistAndMintTokensToUser(from, amountToTransfer);

        // set lock time
        remoraTokenProxy.setLockUpTime(3600);

        // remove `from` from whitelist
        remoraTokenProxy.removeFromWhitelist(from);

        // fund `from` with remora tokens once it is not whitelisted
        remoraTokenProxy.mint(from, amountToTransfer);

        // 10 when was whitelisted and 10 when from was not whitelisted
        assertEq(remoraTokenProxy.balanceOf(from), amountToTransfer * 2);

        // forward beyond the lockup time to demonstrate the removed whitelisted holder can't do transfers
        vm.warp(3600 + 1);

        // reverts because from has only 10 tokens locked
        vm.expectRevert(); // reverts with InsufficientTokensUnlockable
        vm.prank(from);
        remoraTokenProxy.transfer(to, 11);

        // verify from can only transfer the 10 tokens that he received after he was removed from whitelist
        vm.prank(from);
        remoraTokenProxy.transfer(to, 10);
    }
```

**Recommended Mitigation:** A simple and elegant solution may be:
1) check `from` balance; if smaller than `amount` required for transfer revert
2) in transfer functions if the user is not whitelisted, calculate their `uint256 unlockedBalanceToSend = balance - getTokensLocked(sender);` then if `unlockedBalanceToSend < amount` call `_unlockTokens(sender, value - unlockedBalanceToSend..)`;

This solution only attempts to unlock the exact amount needed to fulfill a transfer, and doesn't attempt unlock if nothing to unlock or not required as the user has enough unlocked tokens to fulfill the transfer.

**Remora:** Fixed in commits [67c5e8e](https://github.com/remora-projects/remora-smart-contracts/commit/67c5e8e3262d45f38c18d295a0983dd51f5fd612), [5db7f11](https://github.com/remora-projects/remora-smart-contracts/commit/5db7f11427f6e767a6042c443d552ee9c024494b).

**Cyfrin:** Verified.
