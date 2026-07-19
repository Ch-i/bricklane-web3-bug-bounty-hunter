---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Possible front running of `flag()`
vuln_class: []
---

# Possible front running of `flag()`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** Medium

**Description:** The `target` might call `unstake()/forceUnstake()` before a flagger calls `flag()` to avoid a possible fund loss. Also, there would be no slash during the unstaking for `target` when it meets the `penaltyPeriodSeconds` requirement.

```solidity
File: contracts\OperatorTokenomics\SponsorshipPolicies\VoteKickPolicy.sol
65:     function onFlag(address target, address flagger) external {
66:         require(flagger != target, "error_cannotFlagSelf");
67:         require(voteStartTimestamp[target] == 0 && block.timestamp > protectionEndTimestamp[target], "error_cannotFlagAgain"); // solhint-disable-line not-rely-on-time
68:         require(stakedWei[flagger] >= minimumStakeOf(flagger), "error_notEnoughStake");
69:         require(stakedWei[target] > 0, "error_flagTargetNotStaked"); //@audit possible front run
70:
```

**Impact:** A malicious target would bypass the kick policy by front running.

**Recommended Mitigation:** There is no straightforward mitigation but we could implement a kind of `delayed unstaking` logic for some percent of staking funds.

**Client:** Our current threat model is a staker who doesn't run a Streamr node. They could be a person using Metamask to do all smart contract transactions via our UI, or they could be a complex flashbot MEV searcher. But if they're not running Streamr nodes, they should be found out, flagged, and kicked out by the honest nodes.

While an advanced bot could stake and listen to `Flagged` events, if they're found out and flagged before their minimum stay (`DefaultLeavePolicy.penaltyPeriodSeconds`) is over, their stake would still get slashed even if they front-run the flagging. We aim to select our network parameters so that it will be very likely that someone staking but not actually running a Streamr node would get flagged during those `penaltyPeriodSeconds`. Then front-running the flagging wouldn't save them from slashing.

**Cyfrin:** Acknowledged.
