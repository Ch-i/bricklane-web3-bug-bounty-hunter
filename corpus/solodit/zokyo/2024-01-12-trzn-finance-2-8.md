---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing zero value check for gap in `RiskManagerEscrow_V2`
vuln_class: []
---

# Missing zero value check for gap in `RiskManagerEscrow_V2`

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

There is no check in the `setPara()` function to check that the `_ratio` parameter assigned to the gap variable should not be zero. A zero value assigned to gap can lead to division by zero panic on line: 172. Once the gap amiable is assigned, it cannot be changed again.
```solidity
        return riskManagerEscrowAmt[riskManager][escrowToken] * (10 ** deltaDecimal) * unitRatio / gap;
```
**Recommendation**: 

It is advised to add a zero value check for the gap variable.
