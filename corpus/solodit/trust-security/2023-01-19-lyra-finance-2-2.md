---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-L-3 PoolHedger can receive ETH directly from anyone
vuln_class: []
---

# TRST-L-3 PoolHedger can receive ETH directly from anyone

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
A `receive()` function has been added to GMXFuturesPoolHedger, so that it is able to receive 
ETH from GMX as request refunds. However, it is not advisable to have an open receive() 
function if it is not necessary. Users may wrongly send ETH directly to PoolHedger and lose it 
forever.
```solidity
           receive() external payable {}
``` 
**Recommended Mitigation:**
Add a msg.sender check in the receive() function, and make sure sender is positionRouter.

**Team response:**
Will not be resolved at this stage.
