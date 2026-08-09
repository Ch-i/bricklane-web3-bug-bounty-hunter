---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Wrong validation in `Goldigovernor.cancel()`
vuln_class: []
---

# Wrong validation in `Goldigovernor.cancel()`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** Medium

**Description:** In `Goldigovernor.cancel()`, the proposer should have fewer votes than `proposalThreshold` to cancel his proposal.

```solidity
  function cancel(uint256 proposalId) external {
    if(_getProposalState(proposalId) == ProposalState.Executed) revert InvalidProposalState();
    Proposal storage proposal = proposals[proposalId];
    if(msg.sender != proposal.proposer) revert NotProposer();
    if(GovLocks(govlocks).getPriorVotes(proposal.proposer, block.number - 1) > proposalThreshold) revert AboveThreshold(); //@audit incorrect
    proposal.cancelled = true;
    uint256 targetsLength = proposal.targets.length;
    for (uint256 i = 0; i < targetsLength; i++) {
      Timelock(timelock).cancelTransaction(proposal.targets[i], proposal.eta, proposal.values[i], proposal.calldatas[i], proposal.signatures[i]);
    }
    emit ProposalCanceled(proposalId);
  }
```

**Impact:** A proposer can't cancel his proposal unless he decreases his voting power.

**Recommended Mitigation:** It should be modified like this.

```solidity
if(msg.sender != proposal.proposer && GovLocks(govlocks).getPriorVotes(proposal.proposer, block.number - 1) > proposalThreshold) revert Error;
```

**Client:** Fixed in [PR #7](https://github.com/0xgeeb/goldilocks-core/pull/7)

**Cyfrin:** Verified.
