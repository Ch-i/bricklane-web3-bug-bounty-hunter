---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-2-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[L-05] Reward Distributor implementation uses vulnerable Vyper version'
vuln_class: []
---

# [L-05] Reward Distributor implementation uses vulnerable Vyper version

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

The reward distributor implementation is currently set to use Vyper 0.2.16. This version contains [a vulnerability that prevents reentrancy locks from working properly](https://github.com/vyperlang/vyper/security/advisories/GHSA-5824-cm3x-3c38).

The contract uses `@nonreentrant('lock')` to lock a number of functions. Because of the nature of the vulnerability, each of these locks will lock the specific function from being reentered, but will not prevent a reentrance into another function in the contract.

As an example, if a user was able to gain control flow in the middle of function execution, they could call `claim_rewards()` and, before the latest checkpoint was updated, reenter into `claim_rewards_for()` with the same receiver address and collect the rewards again.

Upon quick review, it appears that the current version is not vulnerable to this attack, because there does not appear to be a vulnerable place where control flow is passed back to the caller mid-execution. However, sufficient time was not spent on this contract (given that it is out of scope) to be sure of that assessment. Further, if Curve were to add a gauge with an extra reward token that contained a callback, this vulnerability would emerge.

**Recommendation**

For safety, it is recommended to upgrade the implementation to the latest Vyper version (0.3.10) before deploying.

In order to make this change, the following upgrades will need to be made:
- `ZERO_ADDRESS` should be changed to`empty(address)`
- `shift(x, y)` should be changed to `x >> y` or `x << y`
- `MAX_UINT256` should be changed to `max_value(uint256)`

While there don't appear to be any other breaking changes [between 0.2.16 and 0.3.10](https://docs.vyperlang.org/en/stable/release-notes.html#v0-2-16) that could cause problems, it is also recommended to include a standard suite of tests for the contract to ensure it continues to behave as expected.

**Review**

Fixed as recommended in commit [a7fc33d1a5351fe8010230d016bb058c3de2b927](https://github.com/stake-dao/only-boost/commit/a7fc33d1a5351fe8010230d016bb058c3de2b927) by upgrading to Liquidity Gauge V4, which uses Vyper 0.3.10 and makes the necessary updates to the source code for it to compile.
