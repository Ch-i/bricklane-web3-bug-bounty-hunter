---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-0-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[H-07] SUP rewards will be completely lost when depositing TBYs to stUSDC
  via wstUSDC'
vuln_class: []
---

# [H-07] SUP rewards will be completely lost when depositing TBYs to stUSDC via wstUSDC

_Section severity (from Solodit section header): High_  
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

When minting stUSDC with tbys the depositor will receive rewards from stUSDC, which are sent to msg.sender.

[WstUsdc.sol#L51-L55](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/WstUsdc.sol#L51-L55)

    function depositTby(uint256 tbyId, uint256 amount) external override returns (uint256 amountMinted) {
        _tby.safeTransferFrom(msg.sender, address(this), tbyId, amount, "");
        amountMinted = _stUsdc.depositTby(tbyId, amount);
        amountMinted = _mintWstUsdc(amountMinted);
    }

We see above that wstUSDC allows direct minting of wstUSDC with tbys. In this case, the wstUSDC contract will be msg.sender and they will be the recipient of the rewards. These rewards are never transferred to the user and will be permanently lost.

**Lines of Code**

[WstUsdc.sol#L51-L55](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/WstUsdc.sol#L51-L55)

**Recommendation**

wstUSDC should check for any rewards and forward them to the user

**Remediation**

Fixed as recommended in stakeup-contracts [PR#94](https://github.com/stakeup-protocol/stakeup-contracts/pull/94)
