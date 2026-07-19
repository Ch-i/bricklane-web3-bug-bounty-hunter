---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-4 Users can lose their entire xMoz balance when specifying too short
  a duration for redemption
vuln_class: []
---

# TRST-M-4 Users can lose their entire xMoz balance when specifying too short a duration for redemption

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
Users can convert their XMoz to Moz through MozStaking, using `redeem()`.
```solidity
            function redeem(uint256 xMozAmount, uint256 duration) external {
                require(xMozAmount > 0, "redeem: xMozAmount cannot be zero");
                    xMozToken.transferFrom(msg.sender, address(this), xMozAmount);
                    uint256 redeemingAmount = xMozBalances[msg.sender];
                   // get corresponding MOZ amount
                    uint256 mozAmount = getMozByVestingDuration(xMozAmount, duration);
                 if (mozAmount > 0) {
             emit Redeem(msg.sender, xMozAmount, mozAmount, duration);
            // add to total
             xMozBalances[msg.sender] = redeemingAmount + xMozAmount;
             // add redeeming entry
                userRedeems[msg.sender].push(RedeemInfo(mozAmount, 
             xMozAmount, _currentBlockTimestamp() + duration));
             }
              }
 ```
If the specified duration is shorter than the minRedeemDuration specified in the staking 
contract, **mozAmount** will end up being zero. In such scenarios, redeem will consume user's 
**xMozAmount** without preparing any redemption at all. The contract should not expose an 
interface that so easily can lead to loss of funds.


**Recommended mitigation:**
If **duration** is less than **minRedeemDuration**, revert the transaction.

**Team response:**
Fixed.

**Mitigation review:**
The staking contract now verifies that the staking duration is safe to use.
