---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-L-6 LiquidityToken owner can freeze all token interactions and suspend
  the platform
vuln_class: []
---

# TRST-L-6 LiquidityToken owner can freeze all token interactions and suspend the platform

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:** 
Owner can freely set the **liquidityTracker** variable in LiquidityToken. It is used in 
`_afterTokenTransfer()`:
```solidity
    function _afterTokenTransfer(address from, address to, uint amount) internal override {
      if (address(liquidityTracker) != address(0)) {
        if (from != address(0)) {
    liquidityTracker.removeTokens(from, amount);
    }
    if (to != address(0)) {
        liquidityTracker.addTokens(to, amount);
           }
         }
       }
```
If owner is compromised, the platform can be immediately shut down by passing an invalid 
address as **liquidityTracker**.

 ### TRST-L-7 Owner can manipulate board’s baseIv
 **Description:** 
In OptionMarket, board characteristics can only be changed when they are frozen. However, 
freezing and unfreezing are done instantly using `setBoardFrozen()`. Therefore, the owner can 
abuse a temporary freeze-unfreeze and inject any sort of malicious behavior, such as setting 
a low baseIv to make personal profit from the protocol. It is advised to put a time lock on 
unfreeze for greater trustability.
