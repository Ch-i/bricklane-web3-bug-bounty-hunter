---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Collateral limit may prevent the position owner from updating their position
  and avoiding liquidation
vuln_class: []
---

# Collateral limit may prevent the position owner from updating their position and avoiding liquidation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

The `updateMargin` function in the Trading contract allows a position owner to either increase or decrease the margin of their open trade. The function retrieves the details of the open trade and performs checks to ensure the caller is the trader of the position and the amount to be added or subtracted is positive. If the margin is being increased, it checks if the new margin would exceed the collateral limit using pairInfo.isExceedGroupsCollateralLimit. If not, it transfers the additional amount from the trader.

However, in a rapidly declining market, the value of collateral can decrease quickly. If the collateral value approaches or exceeds the maximum allowed (as per isExceedGroupsCollateralLimit), traders who wish to add margin to their positions to avoid liquidation may be unable to do so. If traders cannot add margin to their positions, they face automatic liquidation if the margin falls below the maintenance margin.
The check for exceeding the group's collateral limit is not presented during the opening of a position. This inconsistency might allow positions to be opened that are already close to the collateral limit.

**Recommendation**: 

Introduce checks similar to isExceedGroupsCollateralLimit during the position opening phase. This ensures that new positions are not opened too close to the collateral limit, thereby reducing the risk of immediate liquidations in volatile markets.
