---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: '`Goldigovernor._getProposalState()` shouldn''t use `totalSupply`'
vuln_class: []
---

# `Goldigovernor._getProposalState()` shouldn't use `totalSupply`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** Medium

**Description:** In `_getProposalState()`, it uses `Goldiswap(goldiswap).totalSupply()` during the comparison.

```solidity
  function _getProposalState(uint256 proposalId) internal view returns (ProposalState) {
    Proposal storage proposal = proposals[proposalId];
    if (proposal.cancelled) return ProposalState.Canceled;
    else if (block.number <= proposal.startBlock) return ProposalState.Pending;
    else if (block.number <= proposal.endBlock) return ProposalState.Active;
    else if (proposal.eta == 0) return ProposalState.Succeeded;
    else if (proposal.executed) return ProposalState.Executed;
    else if (proposal.forVotes <= proposal.againstVotes || proposal.forVotes < Goldiswap(goldiswap).totalSupply() / 20) { //@audit shouldn't use totalSupply
      return ProposalState.Defeated;
    }
    else if (block.timestamp >= proposal.eta + Timelock(timelock).GRACE_PERIOD()) {
      return ProposalState.Expired;
    }
    else {
      return ProposalState.Queued;
    }
  }
```

As `totalSupply` is increasing in real time, a `Queued` proposal might be changed to `Defeated` one unexpectedly due to the increased supply.

**Impact:** A proposal state might be changed unexpectedly.

**Recommended Mitigation:** We should introduce another mechanism for the quorum check rather than using `totalSupply`.

**Client:** Fixed in [PR #5](https://github.com/0xgeeb/goldilocks-core/pull/5)

**Cyfrin:** Verified.
