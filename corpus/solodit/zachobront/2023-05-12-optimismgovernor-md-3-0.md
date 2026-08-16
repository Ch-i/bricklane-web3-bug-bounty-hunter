---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-12-optimismgovernor-md-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md
tags:
- firm:zachobront
- report:2023-05-12-optimismgovernor-md
title: '[G-01] Loops in ApprovalVotingModule#propose() can be consolidated'
vuln_class: []
---

# [G-01] Loops in ApprovalVotingModule#propose() can be consolidated

_Section severity (from Solodit section header): Gas_  
_Audit firm: ZachObront_  
_Source report: [2023-05-12-OptimismGovernor.md.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md)_

---

In the `propose()` function in `ApprovalVotingModule.sol`, we perform the following two loops:

```solidity
unchecked {
    // Ensure proposal params of each option have the same length between themselves
    ProposalOption memory option;
    for (uint256 i; i < optionsLength; ++i) {
        option = proposalOptions[i];
        if (option.targets.length != option.values.length || option.targets.length != option.calldatas.length) {
            revert InvalidParams();
        }
    }

    // Push proposal options in storage
    for (uint256 i; i < optionsLength; ++i) {
        _proposals[proposalId].options.push(proposalOptions[i]);
    }
}
```

Since these two loops are iterating over the same elements, they can be consolidated into one loop.

**Proof of Concept**

Using the built in test suite's `testProposeWithModule()` function, we can see the following improvement in gas cost:

```
CURRENT IMPLEMENTATION
Running 1 test for test/OptimismGovernorV5.t.sol:OptimismGovernorV5Test
[PASS] testProposeWithModule() (gas: 722324)
Test result: ok. 1 passed; 0 failed; finished in 6.96ms

CONSOLIDATED LOOPS
Running 1 test for test/OptimismGovernorV5.t.sol:OptimismGovernorV5Test
[PASS] testProposeWithModule() (gas: 722048)
Test result: ok. 1 passed; 0 failed; finished in 2.41ms
```

Since this test only uses 2 options, the improvement is minor (`722324 - 722048 = 276`), but this value would be multiplied in proposals with more options.

**Recommendation**

```solidity
unchecked {
    // Ensure proposal params of each option have the same length between themselves
    ProposalOption memory option;
    for (uint256 i; i < optionsLength; ++i) {
        option = proposalOptions[i];
        if (option.targets.length != option.values.length || option.targets.length != option.calldatas.length) {
            revert InvalidParams();
        }
        _proposals[proposalId].options.push(option);
    }
}
```

**Review**

Fixed as recommended in [a89a51559f3b116c60703b2acb2c48bf51121692](https://github.com/voteagora/optimism-gov/commit/a89a51559f3b116c60703b2acb2c48bf51121692).
