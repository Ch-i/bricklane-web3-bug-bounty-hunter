---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-L-2 setPositionRouter leaks approval to previous positionRouter
vuln_class: []
---

# TRST-L-2 setPositionRouter leaks approval to previous positionRouter

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
positionRouter is used to change GMX positions in GMXFuturesPoolHedger. It can be replaced 
by a new router if GMX redeploys, for example if a bug is found or the previous one is hacked. 
The new positionRouter receives approval from the contract. However, approval to the 
previous positionRouter is not revoked.
```solidity
    function setPositionRouter(IPositionRouter _positionRouter) external onlyOwner {
      positionRouter = _positionRouter;
        router.approvePlugin(address(positionRouter));
    emit PositionRouterSet(_positionRouter);
       }
```
A number of unlikely, yet dire scenarios could occur.

**Recommended Mitigation:**
Use router.denyPlugin() to remove privileges from the previous **positionRouter**.

**Team Response:**
By denying the plugin you may also introduce potential issues where a pending position is 
blocked and funds are lost. In the case of a bugged/hacked router, it makes more sense to 
shut off the existing hedger completely and redeploy with relevant changes.

**Trust Security response:**
Point is somewhat correct. Would advise for default behavior to be denyPlugin() in 
setPositionRouter(), with an permissioned approvePlugin() method for unblocking funds.
