---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Staking and withdrawal operations might be blocked.
vuln_class: []
---

# Staking and withdrawal operations might be blocked.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MultiFee Distribution.sol: _stake(), line 644,_withdrawExpiredLocks For(), line 1134. 
During staking and withdrawing funds, a 'beforeLockUpdate hook is called on the Incentives Controller. This hook checks if a user is to be disqualified. For this purpose, the contract performs another external call to Disqualifier.sol, function processUser(). Inside this function, the contract calls an internal function of Disqualifier, _processUserWithBounty(). It has a "require" which will revert if the storage variable 'DISABLED' is set to true. Thus due to this statement on Disqualifier.sol, staking and withdrawing of tokens on MultiFee Distribution.sol might be blocked. 
Further, in_processUserWithBounty(), an external call is performed to ChefIncentivesController.disqualifyUser(), where there are two checks which can also block the operations (Lines 489, 491). 

**Recommendation**: 

Do not revert a whole stake or withdraw transaction due to require statements in the Disqualifier.sol and ChefIncentives Controller.sol. 

**Post-audit**: 

The team removed validations that might prevent staking and withdrawing. However, if a certain user is ineligible for rewards, a bounty should be claimed for him before staking or withdrawing.
