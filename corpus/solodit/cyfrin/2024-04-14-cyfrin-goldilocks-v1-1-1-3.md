---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Users wouldn't cancel their proposals due to the increased `proposalThreshold`.
vuln_class: []
---

# Users wouldn't cancel their proposals due to the increased `proposalThreshold`.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** Medium

**Description:** When users call `cancel()`, it validates the caller's voting power with `proposalThreshold` which can be changed using `setProposalThreshold()`.

```solidity
  function setProposalThreshold(uint256 newProposalThreshold) external {
    if(msg.sender != multisig) revert NotMultisig();
    if(newProposalThreshold < MIN_PROPOSAL_THRESHOLD || newProposalThreshold > MAX_PROPOSAL_THRESHOLD) revert InvalidVotingParameter();
    uint256 oldProposalThreshold = proposalThreshold;
    proposalThreshold = newProposalThreshold;
    emit ProposalThresholdSet(oldProposalThreshold, proposalThreshold);
  }
```

Here is a possible scenario.
- Let's assume `proposalThreshold = 100` and a user has 100 voting power.
- The user has proposed a proposal using `propose()`.
- After that, `proposalThreshold` was increased to 150 by `multisig`.
- When the user calls `cancel()`, it will revert as he doesn't have enough voting power.

**Impact:** Users wouldn't cancel their proposals due to the increased `proposalThreshold`.

**Recommended Mitigation:** It would be good to cache `proposalThreshold` as a proposal state.

**Client:** Acknowledged, we will ensure to only change parameters while there are no pending proposals.

**Cyfrin:** Acknowledged.
