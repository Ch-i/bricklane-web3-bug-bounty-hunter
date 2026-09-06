---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-3
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
title: Chainlink `basePrice` can be non-positive
vuln_class: []
---

# Chainlink `basePrice` can be non-positive

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract Oracle.sol, the method `getPriceFromChainlink(...)` fetches assets prices from chainlink as follows:

```solidity
(
           uint80 roundID,
           int256 basePrice,
           /*uint256 startedAt*/,
           uint256 timeStamp,
           uint80 answeredInRound
       ) =
        AggregatorV3Interface(
           aggregator[_symbol]
       ).latestRoundData();


       if (basePrice == 0) revert ChainlinkMalfunction(TAG, _symbol); 
```
Here `basePrice` is of type int256 meaning it can be a negative value as well. Checking it for just equal to 0 can lead to prices being negative.

**Recommendation**:
Update the above check as follows:
```solidity
if (basePrice <= 0) revert ChainlinkMalfunction(TAG, _symbol);
```
