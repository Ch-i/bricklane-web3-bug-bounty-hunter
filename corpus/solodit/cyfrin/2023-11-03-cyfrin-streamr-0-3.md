---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-0-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Malicious target can make `_endVote()` revert forever by forceUnstaking/staking
  again
vuln_class: []
---

# Malicious target can make `_endVote()` revert forever by forceUnstaking/staking again

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** High

**Description:** In `_endVote()`, we update `forfeitedStakeWei` or `lockedStakeWei[target]` according to the `target`'s staking status.

```solidity
File: contracts\OperatorTokenomics\SponsorshipPolicies\VoteKickPolicy.sol
179:     function _endVote(address target) internal {
180:         address flagger = flaggerAddress[target];
181:         bool flaggerIsGone = stakedWei[flagger] == 0;
182:         bool targetIsGone = stakedWei[target] == 0;
183:         uint reviewerCount = reviewers[target].length;
184:
185:         // release stake locks before vote resolution so that slashings and kickings during resolution aren't affected
186:         // if either the flagger or the target has forceUnstaked or been kicked, the lockedStakeWei was moved to forfeitedStakeWei
187:         if (flaggerIsGone) {
188:             forfeitedStakeWei -= flagStakeWei[target];
189:         } else {
190:             lockedStakeWei[flagger] -= flagStakeWei[target];
191:         }
192:         if (targetIsGone) {
193:             forfeitedStakeWei -= targetStakeAtRiskWei[target];
194:         } else {
195:             lockedStakeWei[target] -= targetStakeAtRiskWei[target]; //@audit revert after forceUnstake() => stake() again
196:         }
```

We consider the target is still active if he has a positive staking amount. But we don't know if he has unstaked and staked again, so the below scenario would be possible.

- The target staked 100 amount and a flagger reported him.
- In `onFlag()`, `lockedStakeWei[target] = targetStakeAtRiskWei[target] = 100`.
- During the voting period, the target called `forceUnstake()`. Then `lockedStakeWei[target]` was reset to 0 in `Sponsorship._removeOperator()`.
- After that, he stakes again and `_endVote()` will revert forever at L195 due to underflow.

After all, he won't be flagged again because the current flagging won't be finalized.

Furthermore, malicious operators would manipulate the above state by themselves to earn operator rewards without any risks.

**Impact:** Malicious operators can bypass the flagging system by reverting `_endVote()` forever.

**Recommended Mitigation:** Perform stake unlocks in `_endVote()` without relying on the current staking amounts.

**Client:** Fixed in commit [8be1d7e](https://github.com/streamr-dev/network-contracts/commit/8be1d7e3ded2d595eaaa16ddd4474d3a8d31bfbe).

**Cyfrin:** Verified.
