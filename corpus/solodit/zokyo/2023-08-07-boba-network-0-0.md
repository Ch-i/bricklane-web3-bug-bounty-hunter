---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: Using oracle method that could return 0
vuln_class: []
---

# Using oracle method that could return 0

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

In contract Boba Deposit Paymaster, function "getTokenValueOfEth" is translating a given value amount of ethereum into the underlying token amount, for that the business logic is using oracles to query for values and different token decimals, oracles will be chosen by the admin of the contract however we expect that most preferred oracles will be BobaStraw, as BobaStraw is a fork of chainlink as it is saying in it's documentation, we noticed that the used function to query the oracles is the function "latestAnswer" which based on it's implementation does not revert if the price returned it's staled or if it can not retrieve the price it will simply return 0 which will break all the logic of the application resulting in a token cost of and and free transactions.

**Recommendation**

Use function "latestRoundData" instead of "latestAnswer" and ensure you are receiving fresh data from it by sanity checking updatedAt and answeredInRound returned values.

**Re-audit comment**

Resolved
