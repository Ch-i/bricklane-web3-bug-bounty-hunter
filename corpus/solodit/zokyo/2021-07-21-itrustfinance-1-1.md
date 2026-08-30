---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-07-21-itrustfinance-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-07-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md
tags:
- firm:zokyo
- report:2021-07-21-itrustfinance
title: Compare to a boolean constant
vuln_class: []
---

# Compare to a boolean constant

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-07-21-ITrustFinance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md)_

---

**Description**

Boolean constants can be used directly and do not need to be compare to true or false.
-require(bool,string)(_paused == false,Contract Frozen) (iTrustInsureV2.sol#122)
-require(bool,string)(purchaseExchange.treasuryAddress != address(0) &&
purchaseExchange.active == true,iTrust: Inactive exchange) (iTrustInsureV2.sol#211-214)
-require(bool)(cover.claimsAllowed == true && _userOwnsCover(userGUID,coverId) == TRUE
&& msg.sender == _userPolicies[userGUID].walletAddress) (iTrustInsureV2.sol#399-401)
-require(bool,string)(cover.iTrustOwned == true,submit NFT) (iTrustInsureV2.sol#398)
-cover.claimed == false (iTrustInsureV2.sol#484)
-cover.claimed == true (iTrustInsureV2.sol#691)

**Recommendation**:
Compare to a boolean constant.
