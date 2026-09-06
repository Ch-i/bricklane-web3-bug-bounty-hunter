---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-12-optimismgovernor-md-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md
tags:
- firm:zachobront
- report:2023-05-12-optimismgovernor-md
title: '[M-02] Any address can be passed as a VotingModule, which could lead to abuse'
vuln_class: []
---

# [M-02] Any address can be passed as a VotingModule, which could lead to abuse

_Section severity (from Solodit section header): Medium_  
_Audit firm: ZachObront_  
_Source report: [2023-05-12-OptimismGovernor.md.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md)_

---

In `OptimismGovernorV5.sol`, the `proposeWithModule()` function has the following signature:

```solidity
function proposeWithModule(VotingModule module, bytes memory proposalData, string memory description);
```

This allows the caller to input a `VotingModule` address, and that module will be used to:

- set up the proposal (`module.propose()`)
- return the execution data (`module._formatExecuteParams()`)
- determine if a user has already voted (`module.hasVoted()`)
- determine if quorum has been reached (`module._quorumReached()`)
- determine whether a vote succeeded (`module._voteSucceeded()`)

It is assumed that the proposer will enter a valid module that does these things fairly, but there is no check to be sure.

This could be abused in a number of ways, but the most malicious and difficult to catch would be to create a module that operates normally but returns malicious data (unrelated to the proposal) from `module._formatExecuteParams()`. Then one could pass an innocent looking proposal, and when it was executed, a completely different transaction would be run. This could be used to perform unwanted actions or steal funds.

While this risk is diminished at the moment because proposals can only be created by the `manager`, it does add some risk at present and will become Critical when governance is opened up to proposals from the community.

**Recommendation**

Create an allowlist of modules that are permitted to be used by the governor, and check that the module is on that list when new proposals are being created.

Fortunately, because the module address is hashed into the `proposalId`, once this value is checked once, it will not need to be checked each time the module is passed.

**Review**

Fixed as recommended in [1152881afcb6272a29e80b0cb17914007a68cd27](https://github.com/voteagora/optimism-gov/commit/1152881afcb6272a29e80b0cb17914007a68cd27).
