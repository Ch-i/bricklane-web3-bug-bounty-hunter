---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Never used imports in multiple contacts.
vuln_class: []
---

# Never used imports in multiple contacts.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Disqualifier.sol: 
ILendingPool, Locked Balance, IUniswapV2Router02, IUniswapV2Factory, IUniswapV2Pair, 
IChainlinkAggregator, IAToken. 
PriceProvider.sol: IERC20, SafeERC20. 
Contracts are imported in files, however they are never used. 

**Recommendation**: 

Remove unnecessary imports OR use them if needed. 

**Post-audit**. 

All unused imports were removed.
