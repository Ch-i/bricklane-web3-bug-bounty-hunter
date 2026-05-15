---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[H-03] Malicious borrower can repeatedly fill then kill orders to permanently
  lock funds of lenders and other borrowers'
vuln_class: []
---

# [H-03] Malicious borrower can repeatedly fill then kill orders to permanently lock funds of lenders and other borrowers

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[Orderbook.sol#L118-L133](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/Orderbook.sol#L118-L133)

    function killBorrowerMatch(address lender) external returns (uint256 lenderAmount, uint256 borrowerReturn) {
        MatchOrder[] storage matches = _userMatchedOrders[lender];

        uint256 len = matches.length;
        for (uint256 i = 0; i != len; ++i) {
            if (matches[i].borrower == msg.sender) {
                lenderAmount = uint256(matches[i].lCollateral);
                borrowerReturn = uint256(matches[i].bCollateral);
                // Zero out the match order to preserve the array's order
                matches[i] = MatchOrder({lCollateral: 0, bCollateral: 0, borrower: address(0)});
                // Decrement the matched depth and open move the lenders collateral to an open order.
                _matchedDepth -= lenderAmount;
                _openOrder(lender, lenderAmount);
                break;
            }
        }

When a borrower kills a match, all values are zeroed out inside the MatchOrder struct and it is kept in the lender's matches array. If this borrower was to match again, they would add yet another entry to the array.

[Orderbook.sol#L252-L265](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/Orderbook.sol#L252-L265)

    if (remainingAmount != 0) {
        uint256 amountToRemove = Math.min(remainingAmount, matches[index].lCollateral);
        uint256 borrowAmount = uint256(matches[index].bCollateral);


        if (amountToRemove != matches[index].lCollateral) {
            borrowAmount = amountToRemove.divWad(_leverage);
            matches[index].lCollateral -= uint128(amountToRemove);
            matches[index].bCollateral -= uint128(borrowAmount);
        }
        remainingAmount -= amountToRemove;
        _idleCapital[matches[index].borrower] += borrowAmount;


        emit MatchOrderKilled(account, matches[index].borrower, amountToRemove);
        if (matches[index].lCollateral == amountToRemove) matches.pop();

When attempting to cancel or match orders, this array is cycled through until the specified amount is canceled/filled. The issue is that if this array is inflated by a malicious borrower then it would cause a OOG DOS. This would result in a permanent loss of funds for the lender as their orders could not be matched or cancelled.

**Lines of Code**

[Orderbook.sol#L118-L139](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/Orderbook.sol#L118-L139)

**Recommendation**

borrower address inside the matches mapping shouldn't be set to address(0). This why repeated fills and kills would only ever result in a single entry per borrower.

**Remediation**

Fixed as recommended in bloom-v2 [PR#15](https://github.com/Blueberryfi/bloom-v2/pull/15)
