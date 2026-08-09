---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-10
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaGovernor::state` incorrectly handles `VetoRatification` proposals'
vuln_class: []
---

# `ArmadaGovernor::state` incorrectly handles `VetoRatification` proposals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `VetoRatification` proposal is passed by default, users should explicitly vote against it to defeat:
```solidity
    function resolveRatification(uint256 ratificationId) external {
        uint256 vetoedId = ratificationOf[ratificationId];
        if (vetoedId == 0) revert Gov_NotARatificationProposal();

        Proposal storage p = _proposals[ratificationId];
        if (block.timestamp <= p.voteEnd) revert Gov_VotingNotEnded();
        if (p.executed) revert Gov_AlreadyResolved();

        p.executed = true;

        // Evaluate outcome: does the community uphold or deny the veto?
        bool quorumMet = _quorumReached(ratificationId);
@>      bool majorityAgainst = quorumMet && (p.againstVotes > p.forVotes);

        if (majorityAgainst) {
            ...
        } else {
@>          // FOR wins or quorum not met → veto stands
            emit RatificationResolved(ratificationId, true);
        }
    }
```

Let's take a look at `state` logic. If quorum is not met, `VetoRatification` proposal succeeds. However `state` returns `Defeated`. Additionally it will return `Defeated` if `QUEUE_GRACE_PERIOD` has passed, however that restriction should not apply to VetoRatification proposals:
```solidity
    /// @notice Get current state of a proposal
    function state(uint256 proposalId) public view returns (ProposalState) {
        Proposal storage p = _proposals[proposalId];
        if (p.id == 0) revert Gov_UnknownProposal();

        if (p.canceled) return ProposalState.Canceled;
        if (p.executed) return ProposalState.Executed;
        if (block.timestamp < p.voteStart) return ProposalState.Pending;
        if (block.timestamp <= p.voteEnd) return ProposalState.Active;

        // After voting ends: check quorum and majority
        if (p.proposalType == ProposalType.Steward) {
            // Pass-by-default: defeated ONLY if quorum met AND strict majority votes against
            if (_quorumReached(proposalId) && p.againstVotes > p.forVotes) {
                return ProposalState.Defeated;
            }
        } else {
@>          if (!_quorumReached(proposalId) || !_voteSucceeded(proposalId)) {
@>              return ProposalState.Defeated;
            }
        }
        ...

        // Succeeded proposals expire if not queued within the grace period
@>      if (block.timestamp > p.voteEnd + QUEUE_GRACE_PERIOD) {
@>          return ProposalState.Defeated;
        }

        return ProposalState.Succeeded;
    }
```

**Impact:** View function `ArmadaGovernor::state` returns incorrect value for `VetoRatification` proposal.

**Recommended Mitigation:** Explicitly handle this case:
```diff
    function state(uint256 proposalId) public view returns (ProposalState) {
        ...
        // After voting ends: check quorum and majority
        if (p.proposalType == ProposalType.Steward) {
            // Pass-by-default: defeated ONLY if quorum met AND strict majority votes against
            if (_quorumReached(proposalId) && p.againstVotes > p.forVotes) {
                return ProposalState.Defeated;
            }
+        } else if (p.proposalType == ProposalType.VetoRatification) {
+           if (_quorumReached(proposalId) && p.againstVotes > p.forVotes) {
+               return ProposalState.Defeated;
+           } else {
+               return ProposalState.Succeeded;
+           }
        } else {
            if (!_quorumReached(proposalId) || !_voteSucceeded(proposalId)) {
                return ProposalState.Defeated;
            }
        }
        ...
    }
```

**Armada:** Fixed in commit [06245ac](https://github.com/ship-armada/armada-poc/commit/06245acd9c135d058c2cba0d4b99ccacf50894cb).

**Cyfrin:** Verified.
