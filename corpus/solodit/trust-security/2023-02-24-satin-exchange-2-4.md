---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-5 _notifyRewardAmount() is incompatible with fee on transfer tokens
vuln_class: []
---

# TRST-L-5 _notifyRewardAmount() is incompatible with fee on transfer tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:** 
The function _notifyRewardAmount() transfers an **amount** of a **token** specified as input to 
itself:
```solidity
           IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
            rewardRate[token] = (amount * PRECISION) / DURATION;
```
After this, it sets the variable **rewardRate[token]** assuming the amount of token received is 
equal to the **amount** it transferred, which is not true in case of tokens that have a fee on 
transfers. This leads to the first users calling `getReward()` to withdraw more tokens than they 
should, and the last user(s) not being able to withdraw at all since the balance is lower than 
expected.

**Recommended mitigation:**
Since only whitelisted tokens are allowed to be used as rewards, the best mitigation is to 
make sure fees on transfer tokens are not whitelisted.

**Team response:**
Added an additional mitigation layer.

**Mitigation Review:**
The team implemented an additional mitigation layer in the function `registerRewardToken()`, 
it’s now only callable by the owner while previously being callable also by users with a 
certain amount of voting power.
