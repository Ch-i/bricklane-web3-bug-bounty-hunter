---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-12-optimismgovernor-md-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md
tags:
- firm:zachobront
- report:2023-05-12-optimismgovernor-md
title: '[M-03] Votes can be arbitrarily extended by Manager until they meet quorum'
vuln_class: []
---

# [M-03] Votes can be arbitrarily extended by Manager until they meet quorum

_Section severity (from Solodit section header): Medium_  
_Audit firm: ZachObront_  
_Source report: [2023-05-12-OptimismGovernor.md.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md)_

---

In `OptimismGovernorV5.sol`, new proposals are created with a `snapshot` (start time) and `deadline` (end time):

```solidity
uint64 snapshot = block.number.toUint64() + votingDelay().toUint64();
uint64 deadline = snapshot + votingPeriod().toUint64();

proposal.voteStart.setDeadline(snapshot);
proposal.voteEnd.setDeadline(deadline);
proposal.votingModule = address(module);
```

All significant parameters on a proposal are locked once the vote is underway:

- a proposal's `votingModule` is immutable and cannot be changed
- updates to `quorum` are saved historically, so that updates don't change existing proposals
- `votingPeriod` and `votingDelay` cannot impact timing because calculations are performed up front and saved
- all settings and options are immutably set and cannot be changed

The one exception is the `proposalDeadline`, which can be edited by the Manager with this function:

```solidity
function setProposalDeadline(uint256 proposalId, uint64 deadline) public onlyManager {
    _proposals[proposalId].voteEnd.setDeadline(deadline);
    emit ProposalDeadlineUpdated(proposalId, deadline);
}
```

This allows the manager to extend the vote for an arbitrary amount of time by continually pushing back the deadline.

This is especially risky when using the `ApprovalVotingModule`, because there are no `Against` votes. If many users are against the proposal, there is no way for them to express their opinion except by not voting. However, extending the vote will inevitably lead to more awareness and a vote that is more likely to pass (either by reaching quorum or by individual options reaching their threshold).

In an extreme case, a Manager could even push back the deadline for a completed vote, reopening it after the fact. In fact, failed votes can be moved from `Defeated` to `Active` at any time. This breaks a strong user assumptions, as votes should be considered final once they are completed.

**Recommendation**

Only allow the deadline to be changed before the vote starts:

```diff
function setProposalDeadline(uint256 proposalId, uint64 deadline) public onlyManager {
+   require(block.timestamp < _proposals[proposalId].voteStart.getDeadline());
    _proposals[proposalId].voteEnd.setDeadline(deadline);
    emit ProposalDeadlineUpdated(proposalId, deadline);
}
```

**Review**

Acknowledged: "Currently leaving this unchanged as `setProposalDeadline` is intended to be unrestricted in this version."
