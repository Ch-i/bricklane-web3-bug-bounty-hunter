---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-12-optimismgovernor-md-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md
tags:
- firm:zachobront
- report:2023-05-12-optimismgovernor-md
title: '[G-02] Remove checks for inaccessible states'
vuln_class: []
---

# [G-02] Remove checks for inaccessible states

_Section severity (from Solodit section header): Gas_  
_Audit firm: ZachObront_  
_Source report: [2023-05-12-OptimismGovernor.md.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md)_

---

`GovernorUpgradeableV2.sol` has a simplified `state()` function that can not reach every possible `ProposalState`.

Here is the enum with the list of possible states:

```solidity
enum ProposalState {
    Pending,
    Active,
    Canceled,
    Defeated,
    Succeeded,
    Queued,
    Expired,
    Executed
}
```

Here is the function, which assigns the state:

```solidity
function state(uint256 proposalId) public view virtual override returns (ProposalState) {
    ProposalCore storage proposal = _proposals[proposalId];

    if (proposal.executed) {
        return ProposalState.Executed;
    }

    if (proposal.canceled) {
        return ProposalState.Canceled;
    }

    uint256 snapshot = proposalSnapshot(proposalId);

    if (snapshot == 0) {
        revert("Governor: unknown proposal id");
    }

    if (snapshot >= block.number) {
        return ProposalState.Pending;
    }

    uint256 deadline = proposalDeadline(proposalId);

    if (deadline >= block.number) {
        return ProposalState.Active;
    }

    if (_quorumReached(proposalId) && _voteSucceeded(proposalId)) {
        return ProposalState.Succeeded;
    } else {
        return ProposalState.Defeated;
    }
}
```

As we can see, Pending, Active, Canceled, Defeated, Succeeded, and Executed states are possible to be reached. However, Queued and Expired are not.

Because much of our function logic is borrowed from versions of the contract where these states were reachable, these values are still checked. We can save some gas by removing the checks for these unreachable states from our functions.

**Recommendation**

In `OptimismGovernorV5.sol#executeWithModule()`, we can remove the check for `Queued`:

```solidity
require(
    status == ProposalState.Succeeded || status == ProposalState.Queued, "Governor: proposal not successful"
);
```

In `OptimismGovernorV5.sol#cancelWithModule()`, we can remove the check for `Expired`:

```solidity
require(
    status != ProposalState.Canceled && status != ProposalState.Expired && status != ProposalState.Executed,
    "Governor: proposal not active"
);
```

In `GovernorUpgradeableV2.sol#execute()`, we can remove the check for `Queued`:

```solidity
require(
            status == ProposalState.Succeeded || status == ProposalState.Queued, "Governor: proposal not successful"
        );
```

In `GovernorUpgradeableV2.sol#_cancel()`, we can remove the check for `Expired`:

```solidity
require(
    status != ProposalState.Canceled && status != ProposalState.Expired && status != ProposalState.Executed,
    "Governor: proposal not active"
);
```

**Review**

Fixed as recommended in [cf1a0ded961f6c617642bb00ed14e3ca87a7a715](https://github.com/voteagora/optimism-gov/commit/cf1a0ded961f6c617642bb00ed14e3ca87a7a715).
