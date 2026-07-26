---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Stale Price Issue in NarwhalPriceAggregator
vuln_class: []
---

# Stale Price Issue in NarwhalPriceAggregator

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity** : Medium

**Status**: Resolved

**Description**

In the NarwhalPriceAggregator smart contract, the function tokenPriceUSDT() queries the latest price for the USDT token using the Pyth Oracle. The function does not perform a check to ensure that the returned price is not stale . As a result, it is possible for the function to return and use outdated pricing information


A price is considered stale when it has not been updated within a certain time threshold, which can be set based on the expected update frequency of the oracle. Stale prices can occur due to delays in updating the price feed or connectivity issues with the oracle.

**Recommendation** :

To address this issue, we recommend implementing a stale price check within the tokenPriceUSDT() function. compare the publishTime field in the priceFeed.price struct with the current block timestamp and define a tolerance (e.g., a few minutes) to account for an acceptable delay in price updates. If the difference between the current timestamp and the publishTime is greater than the tolerance, you can consider the price stale and handle it accordingly (e.g., by reverting the transaction with an error message).

**Fixed**: Issue fixed in commit a72e06b
