---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-7 The protocol might transfer extra SATIN emissions to veSatin holders
  potentially making SatinVoter.sol insolvent
vuln_class: []
---

# TRST-H-7 The protocol might transfer extra SATIN emissions to veSatin holders potentially making SatinVoter.sol insolvent

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `_distribute()` in SatinVoter.sol is generally responsible for distributing weekly 
emissions to a gauge based on the percentage of total votes the associated pool received. In 
particular, it’s called by `updatePeriod()` (as per fix TRST-H-4) on the gauge associated with 
the Satin / $CASH pool.
The variable **veShare** is set to be equal to the returned value of 
`calculateSatinCashLPVeShare()`, which is calculated as the percentage of Satin / $CASH LP 
times **claimable[gauge]** and represents the amount of SATIN that will be transferred to 
VeDist.sol when checkpointing emissions in `checkpointEmissions()`:
```solidity
      uint _claimable = claimable[_gauge];
      if (SATIN_CASH_LP_GAUGE == _gauge) {
            veShare = calculateSatinCashLPVeShare(_claimable);
      _claimable -= veShare;
      }
      if (_claimable > IMultiRewardsPool(_gauge).left(token) && _claimable / DURATION > 0) {
          claimable[_gauge] = 0;
      if (is4poolGauge[_gauge]) {
              IGauge(_gauge).notifyRewardAmount(token, _claimable, true);
      } else {
                IGauge(_gauge).notifyRewardAmount(token, _claimable, false);
           }
      emit DistributeReward(msg.sender, _gauge, _claimable);
        }
```
However, when the if condition (**_claimable > IMultiRewardsPool(_gauge).left(token)** **&&** 
**_claimable / DURATION > 0)** is false the variable **claimable[_gauge]** will not be set to 0, 
meaning the next time veShare will be calculated it will include emissions that have already 
been distributed, potentially making SatinVoter.sol insolvent

**Recommended Mitigation:**
Adjust **claimable[gauge]** after calculating **veShare** and calculate **veShare** only if the 
**msg.sender** is SatinMinter.sol to prevent potential attackers from manipulating the value by 
repeatedly calling _distribute():
```solidity
    if (SATIN_CASH_LP_GAUGE == _gauge && msg.sender == minter) {
        veShare = calculateSatinCashLPVeShare(_claimable);
           claimable[_gauge] -= veShare;
              _claimable -= veShare;
        }
``` 
**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, **claimable[gauge]** is now correctly adjusted and 
the **veShare** calculations are executed only when `_distribute()` is called by SatinMinter.sol.
