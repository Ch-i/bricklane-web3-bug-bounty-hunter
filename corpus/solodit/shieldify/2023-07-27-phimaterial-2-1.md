---
affected_contracts: []
derives_from: []
id: solodit-shieldify-2023-07-27-phimaterial-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-07-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md
tags:
- firm:shieldify
- report:2023-07-27-phimaterial
title: '[L-02] Lack of Consistency and Misleading Naming in Checks'
vuln_class: []
---

# [L-02] Lack of Consistency and Misleading Naming in Checks

_Section severity (from Solodit section header): Low_  
_Audit firm: Shieldify_  
_Source report: [2023-07-27-PHIMaterial.md](https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md)_

---

**Severity**

Low Risk

**Description**

There is a different check implementation in `onlyIfAlreadyClaimed` and `onlyIfAlreadyClaimedMultiple` modifiers for the same check. Additionally, both modifier names ensure that the execution will revert if the user hasn't claimed already but actually, it is the opposite, it reverts if the user has claimed.

**Location of Affected Code**

File: [`src/PhiDaily.sol#L121`](https://github.com/PHI-LABS-INC/DailyMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/PhiDaily.sol#L121)

```solidity
if (dailyClaimedStatus[_msgSender()][eventid][logicid] > 0) {
```

File: [`src/PhiDaily.sol#L134`](https://github.com/PHI-LABS-INC/DailyMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/PhiDaily.sol#L134)

```solidity
if (dailyClaimedStatus[_msgSender()][eventids[i]][logicids[i]] == _CLAIMED) {
```

**Recommendation**

Implement the comparison with the claimed status in both modifiers and correct the naming for sure.

**Team Response**

Acknowledged and fixed as proposed.
