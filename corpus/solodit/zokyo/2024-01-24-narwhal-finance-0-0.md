---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: The undercollateralized positions may avoid being liquidated
vuln_class: []
---

# The undercollateralized positions may avoid being liquidated

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Critical

**Status**: Resolved

**Description**

The stopTrade function in the Trading contract is designed to be called for the liquidation of undercollateralized positions. This function verifies various conditions to ensure a trade can be legitimately closed. These include checking if the trade exists, ensuring compliance with the minimum acceptance delay, and confirming that the closing price has been reached. 
mo
Additionally, the stopTrade function includes a check
```solidity
require(ot.lastUpdateTime + minAcceptanceDelay <= block.timestamp,"wait");
```
which is intended to prevent the premature liquidation of a position. However, this mechanism can be exploited by the position owner.

The contract also includes an updateTPAndSL function, which allows the position owner to update the TP (Take Profit) and SL (Stop Loss) values of their open trades. 
Upon anticipating potential liquidation, the position owner can utilize the updateTPAndSL function to make slight adjustments to the TP/SL values. Each invocation of this function updates the lastUpdateTime of the open trade. Consequently, the owner can continually front-run the liquidation order and advance the lastUpdateTime, effectively preventing the execution of the stopTrade function due to the minAcceptanceDelay condition. This loophole allows the position owner to indefinitely delay the liquidation of an undercollateralized position.

**Recommendation**: 

Consider introducing a separate tracking mechanism for the lastUpdateTime that is only affected by market-related changes, not by TP/SL updates. 
Omit the lastUpdateTime condition if the transaction is intended to liquidate an undercollateralized position.
