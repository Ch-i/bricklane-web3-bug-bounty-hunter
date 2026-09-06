---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Oracle price not always validated
vuln_class: []
---

# Oracle price not always validated

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract Oracle.sol, the method `getPrices(...)` and `getPrice(...)` retrieve price from Chainlink or Uniswap V3.

The returned price values (if stable coin or price fetched from dex) are not always validated to check if it is 0 or within range using the `maxValue` and `minValues`. 

These values are directly used in calculating health factors, and liquidity across the protocol which can lead to unexpected results if the price is set to 0 or not within range.

**Recommendation**: 

It is recommended to validate that the final Oracle price is not 0 and within range if required.
