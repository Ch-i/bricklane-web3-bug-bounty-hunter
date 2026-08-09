---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: In staking contract, resetting self delegation will reset vote weight to zero
vuln_class: []
---

# In staking contract, resetting self delegation will reset vote weight to zero

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** In `TempleGoldStaking` contract, when a delegate resets self delegation, the vote weights delegated to the delegate will be removed by calling `_updateAccountWeight`.
Since zero is passed as new balance parameter, the `stakingTime` of vote weight is reset to zero:
```solidity
// TempleGoldStaking.sol:L580
if (_newBalance == 0) {
    t = 0;
    _lastShares = 0;
}
```

This means that the delegate's vote weight starts accumulating from zero even though the delegate has their own balance, which should not be decreased.

**Impact:** The delegate loses voting power, even becoming zero if resetting self delegation happens right before an epoch ends.

**Recommended Mitigation:** When resetting self delegation, it should not decrease stakeTime so that delegate's voting power remains based on their own balance

**TempleDAO:** Fixed in [PR 1043](https://github.com/TempleDAO/temple/pull/1043)

**Cyfrin:** Verified
