---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-12-optimismgovernor-md-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md
tags:
- firm:zachobront
- report:2023-05-12-optimismgovernor-md
title: '[L-01] Quorum initialized to 0.03% instead of 30% due to overridden denominator'
vuln_class: []
---

# [L-01] Quorum initialized to 0.03% instead of 30% due to overridden denominator

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-05-12-OptimismGovernor.md.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-12-OptimismGovernor.md.md)_

---

When `OptimismGovernorV5.sol` is initialized, the `quorumNumerator` is set to `30`:

```solidity
function initialize(IVotesUpgradeable _votingToken, address _manager) public initializer {
    __Governor_init("Optimism");
    __GovernorCountingSimple_init();
    __GovernorVotes_init(_votingToken);
    __GovernorVotesQuorumFraction_init({quorumNumeratorValue: 30});
    __GovernorSettings_init({initialVotingDelay: 6575, initialVotingPeriod: 46027, initialProposalThreshold: 0});

    manager = _manager;
}
```

This value is intended to represent a 30% quorum when the denominator is set to 100, which is the default value set by OpenZeppelin and is represented in [GovernorVotesQuorumFractionUpgradeableV2.sol#L68-L70](https://github.com/voteagora/optimism-gov/blob/35f441738bd7864bd37949a40842486bc0ac51b0/src/lib/v2/GovernorVotesQuorumFractionUpgradeableV2.sol#L68)

```solidity
function quorumDenominator() public view virtual returns (uint256) {
    return 100;
}
```

However, this value is overriden in `OptimismGovernorV5.sol`:

```solidity
function quorumDenominator() public view virtual override returns (uint256) {
    // Configurable to 3 decimal points of percentage
    return 100_000;
}
```

When quorum is calculated, we perform the following math:

```solidity
function quorum(uint256 blockNumber) public view virtual override returns (uint256) {
    return (token.getPastTotalSupply(blockNumber) * quorumNumerator(blockNumber)) / quorumDenominator();
}
```

The result is that the quorum is represented as `tokenSupply * 30 / 100_000 = tokenSupply * 0.0003`, or 0.03% of supply.

**Proof of Concept**

The following test can be dropped in to `OptimismGovernorV5.t.sol` to show the error:

```solidity
    function testZachQuorumCalculationIncorrect() public {
        uint256 snapshot = block.number + governor.votingDelay();
        vm.roll(snapshot + 1);

        console2.log(op.getPastTotalSupply(snapshot));
        console2.log(governor.quorum(snapshot));
    }
```

```
Logs:
  101000000000000000000 // total supply
  30300000000000000 // quorum (= 0.03% of total supply)
```

**Recommendation**

Change the value set in in the `initialize()` function to `30_000` to represent 30%:

````diff
```solidity
function initialize(IVotesUpgradeable _votingToken, address _manager) public initializer {
    __Governor_init("Optimism");
    __GovernorCountingSimple_init();
    __GovernorVotes_init(_votingToken);
-   __GovernorVotesQuorumFraction_init({quorumNumeratorValue: 30});
+   __GovernorVotesQuorumFraction_init({quorumNumeratorValue: 30_000});
    __GovernorSettings_init({initialVotingDelay: 6575, initialVotingPeriod: 46027, initialProposalThreshold: 0});

    manager = _manager;
}
````

**Review**

Fixed by removing the `initialize()` function (since the proxy has already been initialized and is just being upgraded) in [6aa306ea5df526bd49e88073daa0da27c5b56e5e](https://github.com/voteagora/optimism-gov/commit/6aa306ea5df526bd49e88073daa0da27c5b56e5e)
