---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-10 canHedge will return true when trade moves delta in same direction
  as expectedHedge even when that leads to more risk
vuln_class: []
---

# TRST-M-10 canHedge will return true when trade moves delta in same direction as expectedHedge even when that leads to more risk

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
Lyra’s security model relies on being able to hedge and achieve delta-neutrality when opening 
a user position. The check is done in canHedge() in GMXFuturesPoolHedger. The function will 
return true when the delta of the trade has the same sign as the expectedHedge. For example:
```solidity 
    // expected hedge is positive, and trade increases delta of the pool - risk is reduced, so accept trade
    if (increasesPoolDelta && expectedHedge >= 0) {
        return true;
          }
```
However, this will not always reduce the pool delta. For example an **expectedHedge** of 5 
would indicate the pool delta is -5. A trade which increases pool delta by 11 would mean the 
subsequent **expectedHedge** would be -6. In general, if the **expectedHedge** is equal to n/-n 
then a trade which increases/decreases pool delta by greater than 2*n will increase risk. 

**Recommended mitigation:**
Take the magnitude of the trade size into account when performing this check.

**Team response:**
Valid, but the additional complexity is too much to add at this stage when benefits are 
minimal. The inclusion of `strikeId` to the canHedge function will enable more detailed checks 
that check the exact delta risk added to be added in the future.
