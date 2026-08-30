---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md
tags:
- firm:zokyo
- report:2021-06-14-impossible-finance
title: Functions should be declared as external
vuln_class: []
---

# Functions should be declared as external

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

ImpossiblePair.getFeeAndXybk() (ImpossiblePair.sol#67-70)
ImpossiblePair.updateGovernance(address) (ImpossiblePair.sol#140-143)
ImpossiblePair.makeXybk(uint8,uint8,uint32,uint32) (ImpossiblePair.sol#146-169)
ImpossiblePair.makeUni() (ImpossiblePair.sol#173-183)
ImpossiblePair.updateTradeFees(uint16) (ImpossiblePair.sol#185-190)
ImpossiblePair.updateDelay(uint256) (ImpossiblePair.sol#194-198)
ImpossiblePair.updateHardstops(uint8,uint8) (ImpossiblePair.sol#201-207)
ImpossiblePair.updateBoost(uint32,uint32) (ImpossiblePair.sol#210-221)
ImpossibleRouter01.quote(uint256,uint256,uint256) (ImpossibleRouter01.sol#344-350)
ImpossibleRouter02.quote(uint256,uint256,uint256) (ImpossibleRouter02.sol#470-476)
ImpossibleRouter01.getAmountOut(uint256,address,address)
(ImpossibleRouter01.sol#352-358)
ImpossibleRouter02.getAmountOut(uint256,address,address)
(ImpossibleRouter02.sol#478-484)
ImpossibleRouter01.getAmountIn(uint256,address,address)
(ImpossibleRouter01.sol#360-366)
ImpossibleRouter02.getAmountIn(uint256,address,address)
(ImpossibleRouter02.sol#486-492)
ImpossibleRouter01.getAmountsOut(uint256,address[]) (ImpossibleRouter01.sol#369-376)
ImpossibleRouter02.getAmountsOut(uint256,address[]) (ImpossibleRouter02.sol#494-502)
ImpossibleRouter01.getAmountsIn(uint256,address[]) (ImpossibleRouter01.sol#379-386)
ImpossibleRouter02.getAmountsIn(uint256,address[]) (ImpossibleRouter02.sol#504-512)

**Recommendation**:

Functions should be declared as external
