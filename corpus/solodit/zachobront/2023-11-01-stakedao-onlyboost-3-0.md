---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[I-01] Strong trust assumption that Convex will act in good faith'
vuln_class: []
---

# [I-01] Strong trust assumption that Convex will act in good faith

_Section severity (from Solodit section header): Informational_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

There are a number of trust assumptions in the protocol that assume that Convex will act in good faith. Specifically, Convex has control over data returned from various functions which could be altered to influence the behavior of the strategy.

For example:

1) When claiming extra reward tokens from Convex, we assume that the data returned from `baseRewardPool.extraRewards(i)` is accurate. Convex could clear the list of extra reward tokens from the `baseRewardPool`, call `claim()` on the StakeDAO contract (skipping the extra rewards), and then re-add the tokens to the list — effectively skirting around paying these rewards to StakeDAO.

2) We assume that `ERC20(gauge).balanceOf(VOTER_PROXY_CONVEX)` will accurately reflect the amount of gauge token held by Convex. However, there may be ways for them to temporarily alter this value to throw off the optimization.

3) There are some quirks in the balancing of deposits and withdrawals between Convex and StakeDAO (discussed in other issues). These quirks could be used to consistently move funds towards a high allocation on Convex and away from StakeDAO.

**Recommendation**

Set up monitoring solutions to ensure the protocol is behaving as expected, with flags to warn you of any of the scenarios that might point to Convex manipulating the strategy.

**Review**

Acknowledged.
