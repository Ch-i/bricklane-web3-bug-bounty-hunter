---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Contracts can be initialized with wrong parameters.
vuln_class: []
---

# Contracts can be initialized with wrong parameters.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MultiFee Distribution.sol: initialize(). 
TokenVesting.sol: initialize(), _notifyUnseenReward() 
1. MultiFee Distribution.sol: No parameters are being validated in initialize(). This might be a serious problem as addresses "mfdStats" and "priceProvider" do not have setters themselves as the variables REWARDS_DURATION, REWARDS_LOOKBACK, DEFAULT_LOCK_DURATION do not have setter either and are set only in initialize() method. 
2. TokenVesting.sol: rdntToken is not validated against zero address in initialize() method and there is no setter for rdntToken variable. 
3. Eligibility DataProvider.sol, Disqualifier.sol, Leverager.sol, PriceProvider.sol: all address parameters should be validated against zero addresses in constructor and initializer 
4. MultiFee Distribution.sol: _notify Unseen Reward(): At line 965 subtraction 
REWARDS_DURATION - REWARDS_LOOKBACK might underflow in case REWARDS_LOOKBACK is greater than REWARDS_DURATION. Thus the initiaize() function should verify that subtraction won't result in an underflow. 
5. RadiantOFT.sol: parameters_endpoint and_treasury in constructor should be validated against zero address. _fee should be validated not to exceed 1e4. 
6. StargateBorrow.sol: all address parameters. _xChainBorrow FeePercent not to exceed 1e4. 

**Recommendation**: 

Validate parameters in initialization of contracts. 

**Post-audit**: 

All validations were added.
