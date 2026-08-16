---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-8 Calculation of the new emissions amount is not 75%/25%/5%
vuln_class: []
---

# TRST-M-8 Calculation of the new emissions amount is not 75%/25%/5%

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The calculations of the emissions directed to SatinVoter.sol, VeDist.sol, and the treasury are 
done on top of the weekly emissions instead as part of it, resulting in a different percentage 
distribution. The calculations are as follows:
```solidity
    uint _weekly = WEEKLY_EMISSION;
         WEEKLY_EMISSION =(_weekly * _WEEKLY_EMISSION_DECREASE) / _WEEKLY_EMISSION_DECREASE_DENOMINATOR;
    uint _growth = _calculateGrowth(_weekly);
        uint _required = _growth + _weekly;
```
Where **growthDivider**** is set to 20, **toTreasuryDivider** is set to 5 and **_required** is the total 
amount of tokens that will be distributed. Let’s suppose **_weekly** is 1000, **_growth** will be set 
to 50, **_toTeam** to 200, and **_required** to 1250. The distribution would result in 80% to 
SatinVoter.sol, 16% to the treasury, and 4% to VeDist.sol. This results in veSatin holders 
receiving fewer rewards (in relative value) than voters. 

**Recommended mitigation:**
Set **_required** equal to **_weekly** and calculate the amount of emissions to send to 
SatinVoter.sol as the **_weekly** amount minus the emissions sent to treasury and VeDist.sol:
```solidity
        uint _required = _weekly;
    // …snippet…
           token.approve(address(_voter()), _weekly - _growth - _toTeam);
    _voter().notifyRewardAmount(_weekly - _growth - _toTeam);
```
**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, now the calculations of the emissions are done as 
part of the weekly emissions amount instead of on top of it.
