---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[H-01] BloomPool#redeemBorrower fails to decrement \_idToTotalBorrowed leading
  to large portions of borrower funds being permanently trapped in the contract'
vuln_class: []
---

# [H-01] BloomPool#redeemBorrower fails to decrement \_idToTotalBorrowed leading to large portions of borrower funds being permanently trapped in the contract

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[BloomPool.sol#L133-L136](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L133-L136)

    uint256 totalBorrowAmount = _idToTotalBorrowed[id];
    uint256 borrowAmount = _borrowerAmounts[msg.sender][id];

    reward = (_tbyBorrowerReturns[id] * borrowAmount) / totalBorrowAmount;

Rewards for borrower is calculated by taking borrower's share of total borrow and dividing returns evenly.

[BloomPool.sol#L137-L144](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L137-L144)

    require(reward > 0, Errors.ZeroRewards());

    _idToCollateral[id].assetAmount -= uint128(reward);
    _tbyBorrowerReturns[id] -= reward;
    _borrowerAmounts[msg.sender][id] -= borrowAmount;

    emit BorrowerRedeemed(msg.sender, id, reward);
    IERC20(_asset).safeTransfer(msg.sender, reward);

We see above that `_tbyBorrowerReturns` are decremented but `_idToTotalBorrowed` is not. This leads to diminishing rewards share. Take the following example, if there is 1000 borrowed evenly between two users and there are 100 returns. We would expect that 50 would be claimable by each user though this will not be the case. For first user claim:

    reward = 100 * 500 / 1000 = 50

After the claim `_tbyBorrowerReturns` == 50 `_idToTotalBorrowed` == 1000 so for the second claim:

    reward = 50 * 500 / 1000 = 25

We see the reward is incorrect and 25% of total rewards are now trapped permanently in the contract

**Lines of Code**

[BloomPool.sol#L132-L145](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L132-L145)

**Recommendation**

\_idToTotalBorrowed should be decremented by borrowAmount to keep reward rate constant across

**Remediation**

Fixed as recommended in bloom-v2 [PR#14](https://github.com/Blueberryfi/bloom-v2/pull/14)
