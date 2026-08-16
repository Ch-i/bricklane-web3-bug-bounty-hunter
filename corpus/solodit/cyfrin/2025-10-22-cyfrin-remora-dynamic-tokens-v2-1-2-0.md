---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Self transfer of all child tokens results in decement of `ChildToken.totalInvestors`
  storage variable
vuln_class: []
---

# Self transfer of all child tokens results in decement of `ChildToken.totalInvestors` storage variable

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** Similar to Issue [*Frontrunning call to `ChildToken::resolveUser` and transferring all of the oldUser's `childToken` balance causes the `totalInvestor` counter to be decremented twice*](#frontrunning-call-to-childtokenresolveuser-and-transferring-all-of-the-oldusers-childtoken-balance-causes-the-totalinvestor-counter-to-be-decremented-twice), if `user` calls `ChildToken::transfer(user, <balance of user>)` this will result in `totalInvestors` being decremented.

This is because the override of `_update` determines the decrements/increments based on the balance _before_ the transfer.

```solidity
    function _update(
        address from,
        address to,
        uint256 value
    ) internal override {
@1>     if (from != address(0) && balanceOf(from) - value == 0) --totalInvestors;
@2>     if (to != address(0) && balanceOf(to) == 0) ++totalInvestors;
...
```

- Line `@1>` causes the `totalInvestors` to be decremented, but
- Line `@2>` does not cause an increment since `balanceOf(to)` is the before-transfer balance


**Impact:** The impact is minimal in most cases, as `totalInvestors` is only used for informational purposes.
However, if it is done enough times it will lead to underflows precisely when:
- `totalInvestors == 0`, and
- a user is transferring all their tokens to another user

**Proof of Concept:** Add the following test to `CentralTokenTest.t.sol`

```solidity

    function test_cyfrin_selfTransferDecrements() public {
        address user = getDomesticUser(1);
        uint32 DEFAULT_LOCK_TIME = 365 days;

        // Seed: old user has 3 tokens (locked by default on mint)
        centralTokenProxy.mint(address(this), uint64(3));
        centralTokenProxy.dynamicTransfer(user, 3);
        assertEq(d_childTokenProxy.balanceOf(user), 3);
        assertEq(d_childTokenProxy.totalInvestors(), 1);

        vm.warp(block.timestamp + DEFAULT_LOCK_TIME); // warp to unlock tokens
        vm.prank(user);
        d_childTokenProxy.transfer(user, 3);

        assertEq(d_childTokenProxy.totalInvestors(), 0);
        assertEq(d_childTokenProxy.balanceOf(user), 3);

        // Do it one more time and we get a revert
        vm.warp(block.timestamp + DEFAULT_LOCK_TIME);  // warp to unlock tokens
        vm.prank(user);
        vm.expectRevert(); // expect underflow
        d_childTokenProxy.transfer(user, 3);
    }
```

**Recommended Mitigation:** If `from == to` do nothing to the investor count.

```diff
+       if (from != to) {
            if (from != address(0) && balanceOf(from) - value == 0) --totalInvestors;
            if (to != address(0) && balanceOf(to) == 0) ++totalInvestors;
+       }

        super._update(from, to, value);
```

**Remora:** Fixed at commit [b612c87](https://github.com/remora-projects/remora-dynamic-tokens/commit/b612c8735b9da1e563af7b0071f3da0c67d60702).

**Cyfrin:** Verified. `totalInvestors` counter is not modified if `from` and `to` are the same address.
