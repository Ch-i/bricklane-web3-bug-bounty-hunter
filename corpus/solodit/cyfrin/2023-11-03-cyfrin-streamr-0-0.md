---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: '`VoteKickPolicy._endVote()` might revert forever due to underflow'
vuln_class: []
---

# `VoteKickPolicy._endVote()` might revert forever due to underflow

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** High

**Description:** In `onFlag()`, `targetStakeAtRiskWei[target]` might be less than the total rewards for the flagger/reviewers due to rounding.

```solidity
File: contracts\OperatorTokenomics\StreamrConfig.sol
22:     /**
23:      * Minimum amount to pay reviewers+flagger
24:      * That is: minimumStakeWei >= (flaggerRewardWei + flagReviewerCount * flagReviewerRewardWei) / slashingFraction
25:      */
26:     function minimumStakeWei() public view returns (uint) {
27:         return (flaggerRewardWei + flagReviewerCount * flagReviewerRewardWei) * 1 ether / slashingFraction;
28:     }
```

- Let's assume `flaggerRewardWei + flagReviewerCount * flagReviewerRewardWei = 100, StreamrConfig.slashingFraction = 0.03e18(3%), minimumStakeWei() = 1000 * 1e18 / 0.03e18 = 10000 / 3 = 3333.`
- If we suppose `stakedWei[target] = streamrConfig.minimumStakeWei()`, then `targetStakeAtRiskWei[target] = 3333 * 0.03e18 / 1e18 = 99.99 = 99.`
- As a result, `targetStakeAtRiskWei[target]` is less than total rewards(=100), and `_endVote()` will revert during the reward distribution due to underflow.

The above scenario is possible only when there is a rounding during `minimumStakeWei` calculation. So it works properly with the default `slashingFraction = 10%`.

**Impact:** The `VoteKickPolicy` wouldn't work as expected and malicious operators won't be kicked forever.

**Recommended Mitigation:** Always round the `minimumStakeWei()` up.

**Client:** Fixed in commit [615b531](https://github.com/streamr-dev/network-contracts/commit/615b5311963082c79d05ec4072b1abeba4d1f9b4).

**Cyfrin:** Verified.
