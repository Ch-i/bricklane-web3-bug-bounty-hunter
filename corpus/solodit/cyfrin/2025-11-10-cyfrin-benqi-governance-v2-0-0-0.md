---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Distribution logic can be broken by upgrades to the `GaugeRegistrar` by the
  DAO to add logic to modify the `enableUpdateVotingPowerHook` configuration
vuln_class: []
---

# Distribution logic can be broken by upgrades to the `GaugeRegistrar` by the DAO to add logic to modify the `enableUpdateVotingPowerHook` configuration

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `DistributionManager` contract hardcodes epoch 0 when reading gauge votes from the `AddressGaugeVoter ` contract within `_collectVotes()`:

```solidity
function _collectVotes() internal view returns (...) {
    ...
    for (uint256 j = 0; j < gaugeAddresses.length; j++) {
        address gaugeAddress = gaugeAddresses[j];
        IGaugeRegistrar.RegisteredGauge memory gaugeInfo = gaugeRegistrar.getGaugeInfo(gaugeAddress);

@>      uint256 votes = gaugeVoter.epochGaugeVotes(0, gaugeAddress);

        gaugesByController[i][j] = IDistributionGaugeVote.GaugeVote({
            gaugeAddress: gaugeAddress,
            qiToken: gaugeInfo.qiToken,
            incentive: gaugeInfo.incentive,
            votes: votes
        });
        voteTotals[i] += votes;
    }
}
```

However, `AddressGaugeVoter` conditionally stores votes in either epoch 0 or the current epoch based on the `enableUpdateVotingPowerHook` configuration flag:

```solidity
function _vote(address _account, GaugeVote[] memory _votes) internal {
    ...
    uint256 epoch = getWriteEpochId(); // ← Uses conditional epoch
    AddressVoteData storage voteData = epochVoteData[epoch][_account];
    ...
}

function getWriteEpochId() public view returns (uint256) {
    return enableUpdateVotingPowerHook ? 0 : epochId();
}
```

The system assumes `enableUpdateVotingPowerHook` is always true, storing votes in epoch 0, but:
1. This setting can be changed via calls to `setEnableUpdateVotingPowerHook()` by the `GAUGE_ADMIN_ROLE`.
2. There is no validation during deployment or runtime to enforce this assumption.
3. If set to false, votes are stored in the current epoch (1, 2, 3, ...) but `DistributionManager` always reads from epoch 0.

Regarding calls to `AddressGaugeVoter::setEnableUpdateVotingPowerHook` by the `GAUGE_ADMIN_ROLE`, the `GaugeRegistrar` is granted this permission but the functionality is not currently implemented. However, the `GAUGE_REGISTRAR_ROLE` is granted to the DAO which would allow the implementation to be upgraded and potentially add some logic that violates the assumption that this configuration cannot be changed for BENQI.

**Impact:** If the `enableUpdateVotingPowerHook` configuration is changed by the DAO, all calls to `distribute()` will erroneously read votes from 0 epoch, resulting in incorrect reward calculations.

**Recommended Mitigation:** Either explicitly forbid this configuration from being modified or consider modifying the vote collection logic to conditionally retrieve the current epoch if `enableUpdateVotingPowerHook` is false.

**BENQI:** The `AddressGaugeVoter` should leave the `setEnableVotingPower` enabled as it's the default setting for the Aragon Escrow system. The DAO will be the shared owner, by default of both the address gauge voter and the gauge registrar, both of which are UUPS. It is correct that this means the registrar could be upgraded and then can make administrative calls to the voter outside the scope of gauge registration as it is the admin. In practice, for BENQI, the DAO will be the same entity so if it's compromised in one place it's compromised in the other anyway. This logic is confirmed in the `DistributionManagerSetup` which reverts if the DAO mismatches between the voter and the `DistributionManager`. Fixed in commit [3ab793e](https://github.com/aragon/benqi-governance/pull/25/commits/3ab793e0115d3595f95400b55e43d9e1693da0a8) and PR [\#20](https://github.com/aragon/benqi-governance/pull/20).

**Cyfrin:** Verified. Separation has been added to the operational and administrative `GaugeRegistrar` roles. `DistributionManager::_validateCanDistribute` also now reverts if `GaugeVoter::enableUpdateVotingPowerHook` is disabled.
