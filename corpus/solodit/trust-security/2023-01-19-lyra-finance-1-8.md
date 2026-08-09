---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-9 canHedge may return true when there is insufficient GMX liquidity
  to facilitate hedging, causing insolvency risks
vuln_class: []
---

# TRST-M-9 canHedge may return true when there is insufficient GMX liquidity to facilitate hedging, causing insolvency risks

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
Lyra’s security model relies on being able to hedge and achieve delta-neutrality when opening 
a user position. The check is done in canHedge() in GMXFuturesPoolHedger. After expected 
hedge delta and current hedge delta are fetched, remainingDeltas is assigned the amount of 
liquidity of the side that will be bought. Then this check is made:
```solidity
      uint absHedgeDiff = (Math.abs(expectedHedge) - Math.abs(currentHedge));
      if (remainingDeltas < 
           absHedgeDiff.multiplyDecimal(futuresPoolHedgerParams.marketDepthBuffer)) {
        return false;
      }

```
The issue is that the checked requirement for GMX liquidity is not strict enough. If 
**expectedHedge** and **currentHedge** have different signs, **remainingDeltas** needs to be above 
**expectedHedge**. That’s because the current holdings can’t be deducted from the necessary 
delta. The impact is that the function would approve sign-switching hedges more leniently 
than it should.

**Recommended mitigation:**
Check if **expectedHedge** and **currentHedge** have different signs and change logic accordingly.

**Team response:**
Valid; but similar to **H-1** canHedge is more a safety rail than a core requirement of system 
operation. The **deltaThreshold** parameter will cause the hedger to be updated more 
frequently if the hedged delta and expected delta diverge by a large enough amount - which 
will make these checks operate as expected. Will not be resolved at this stage.
