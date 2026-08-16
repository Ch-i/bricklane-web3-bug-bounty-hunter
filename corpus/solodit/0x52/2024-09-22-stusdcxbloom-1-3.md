---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[M-04] stUSDC#deposit compares current tby price with potentially stale pool
  price which can lead to small yield loss for pool'
vuln_class: []
---

# [M-04] stUSDC#deposit compares current tby price with potentially stale pool price which can lead to small yield loss for pool

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[StUsdc.sol#L154-L157](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L154-L157)

    function poke() external nonReentrant {
        uint256 currentTimestamp = block.timestamp;
        uint256 lastUpdate = _lastRateUpdate;
        if (currentTimestamp - lastUpdate < 24 hours) return;

stUSDC#poke syncs the value of the pool and as we see above, this is limited to one update every 24 hours.

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

This is generally fine but can lead to tbys being relatively overvalued. If the pool has gone 12 hours without syncing, there will be 12 hours worth of value that has accumulated but that has not been accounted for. Meanwhile we see that during deposit, it pulls a fresh exchange rate from the pool. This difference will cause the tby being deposited to be slightly overvalued compared to an exact same tby in the pool.

**Lines of Code**

[StUsdc.sol#L118-L130](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L118-L130)

**Recommendation**

The tby rate should be adjusted to exclude yield that has accumulated since the last poke (i.e. if it's been 12 hours since poke, 12 hours of yield should be deducted).

**Remediation**

Fixed in stakeup-contracts [PR#96](https://github.com/stakeup-protocol/stakeup-contracts/pull/96)
