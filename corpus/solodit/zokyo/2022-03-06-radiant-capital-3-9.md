---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-9
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Disqualification mechanism should be verified.
vuln_class: []
---

# Disqualification mechanism should be verified.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Disqualifier.sol: _processUserWithBounty(). 
ChefIncentivesController.sol: disqualify User(), _isEligible(). 
In Disqualifier.sol (lines 167-168), the user will be disqualified from ChefIncentivesController.sol if the user's unlockable > 0 and either relock is disabled or the user's locked value is less than his collateral value in Lending Pool. 
Thus, the user is considered ineligible in case 'lastEligibleTime > block.timestamp && ! eligibility Provider.isEligible ForRewards(_user) (Disqualifier.sol, line 163.). However, in ChefIncentivesController.disqualifyUser(), the user is considered ineligible for rewards if lastEligibleTime < block.timestamp OR !eligibility Provider.isEligible ForRewards(_user) (It is checked in line 491 by calling!_isEligible()). Due to this mismatch, the transaction might fail. 
Also, disqualification may be called on ChefIncentives Controller in case relock is disabled or in case chef bounty > 0 (line 180). However, in this case, relock from ChefIncentivesController is not taken into account. Thus, if the user is ineligible due to relock, it will not disqualify him on ChefIncentives Controller, reverting the whole transaction due to check on line 491. 
In Disqualifier.sol, line 191, eligibility is also checked after locks might be withdrawn, which can affect the result of eligibility Provider.is Eligible For Rewards(). Thus, it should be verified if such functionality is correct, or eligibility should be tracked before the locks are withdrawn. 

**Recommendation**: 

Verify the correctness of the current disqualification mechanism and that its implementation corresponds to business logic. Make sure that transaction won't revert due to mismatching validations on Disqualifier.sol and ChefIncentives Controller.sol. 

**Post-audit**: 

Disqualification mechanism was updated. All logic, connected to disqualifications and bounty is executed in ChefIncentivesController or MFDPlus.
