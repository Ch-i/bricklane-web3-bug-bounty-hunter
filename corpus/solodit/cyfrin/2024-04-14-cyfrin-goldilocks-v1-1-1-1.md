---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: In `Goldivault.redeemYield()`, users can redeem more yield tokens using reentrancy
vuln_class: []
---

# In `Goldivault.redeemYield()`, users can redeem more yield tokens using reentrancy

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** Medium

**Description:** Possible reentrancy in `Goldivault.redeemYield()` if `yieldToken` has a `beforeTokenTransfer` hook.

- Let's assume `yt.totalSupply = 100, yieldToken.balance = 100` and the user has 20 yt.
- The user calls `redeemYield()` with 10 yt.
- Then `yt.totalSupply` will be changed to 90 and it will transfer `100 * 10 / 100 = 10 yieldToken` to the user.
- Inside the `beforeTokenTransfer` hook, the user calls `redeemYield()` again with 10 yt.
- As `yieldToken.balance` is still 100, he will receive `100 * 10 / 90 = 11 yieldToken`.

```solidity
  function redeemYield(uint256 amount) external {
    if(amount == 0) revert InvalidRedemption();
    if(block.timestamp < concludeTime + delay || !concluded) revert NotConcluded();
    uint256 yieldShare = FixedPointMathLib.divWad(amount, ERC20(yt).totalSupply());
    YieldToken(yt).burnYT(msg.sender, amount);
    uint256 yieldTokensLength = yieldTokens.length;
    for(uint8 i; i < yieldTokensLength; ++i) {
      uint256 finalYield;
      if(yieldTokens[i] == depositToken) {
        finalYield = ERC20(yieldTokens[i]).balanceOf(address(this)) - depositTokenAmount;
      }
      else {
        finalYield = ERC20(yieldTokens[i]).balanceOf(address(this));
      }
      uint256 claimable = FixedPointMathLib.mulWad(finalYield, yieldShare);
      SafeTransferLib.safeTransfer(yieldTokens[i], msg.sender, claimable);
    }
    emit YieldTokenRedemption(msg.sender, amount);
  }
```

**Impact:** Malicious users can steal `yieldToken` using `redeemYield()`.

**Recommended Mitigation:** We should add a `nonReentrant` modifier to `redeemYield()`.

**Client:** Fixed in [PR #13](https://github.com/0xgeeb/goldilocks-core/pull/13)

**Cyfrin:** Verified.
