---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-1-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[M-06] SUP rewards for depositing TBYs can be gamed by depositing TBYs that
  are close to expiration'
vuln_class: []
---

# [M-06] SUP rewards for depositing TBYs can be gamed by depositing TBYs that are close to expiration

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[StUsdc.sol#L118-L130](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L118-L130)

    function depositTby(uint256 tbyId, uint256 amount) external nonReentrant returns (uint256 amountMinted) {
        IBloomPool pool = _bloomPool;
        require(amount > 0, Errors.ZeroAmount());
        require(!pool.isTbyRedeemable(tbyId), Errors.RedeemableTbyNotAllowed());
        // If the token is a TBY, we need to get the current exchange rate of the token
        //     to accurately calculate the amount of stUsdc to mint.
        amountMinted = pool.getRate(tbyId).mulWad(amount) * _scalingFactor;
        _deposit(amountMinted);
        _mintRewards(amountMinted);

        emit TbyDeposited(msg.sender, tbyId, amount, amountMinted);
        _tby.safeTransferFrom(msg.sender, address(this), tbyId, amount, "");
    }

When minting via `stUSDC#depositTBY`, rewards are paid out based on `amountMinted`. The goal of this reward is to incentivize users to deposit, thereby generating increased TVL for the protocol. This mechanism, however, can be gamed by depositing tbys that are very close to expiration. Due to the rate scaling these tbys will qualify for a large amount of shares while contributing very little to the yield.

**Lines of Code**

[StUsdc.sol#L118-L130](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L118-L130)

**Recommendation**

Rewards paid should be proportional to the length of time left until maturity. The closer they are to maturity, the less rewards should be paid.

**Remediation**

Fixed as recommended in stakeup-contracts [PR#87](https://github.com/stakeup-protocol/stakeup-contracts/pull/87)
