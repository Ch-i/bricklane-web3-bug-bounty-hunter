---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: No Price Staleness Check
vuln_class: []
---

# No Price Staleness Check

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity** - Medium

**Status** - Resolved

**Description**

The function `latestRoundData()` has been used inside ERC20PriceOracle_V2 (getChainlinkPrice) to fetch the price of an asset , but there are no price staleness checks.



**Recommendation**:

Introduce price staleness checks as follows →
```solidity
(uint80 roundID, int256 answer, , uint256 timestamp, uint80 answeredInRound) = tokenInfos[token].chainlinkOracle.latestRoundData();
require(answeredInRound >= roundID, "Stale price");
require(timestamp != 0,"Round not complete");
```
