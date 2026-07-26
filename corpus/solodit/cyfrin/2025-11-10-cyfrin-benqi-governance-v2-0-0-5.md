---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-5
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
title: Single `rewardToken` design is incompatible with multi-reward emission support
vuln_class: []
---

# Single `rewardToken` design is incompatible with multi-reward emission support

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `BenqiEcosystemModule` assumes QI as the single immutable `rewardToken` always referenced directly within `_processGauge()`:

```solidity
 function _processGauge(
    IMultiRewardDistributor _distributor,
    GaugeVote memory _gauge,
    uint256 _totalVotes,
    uint256 _budget,
    uint256 _epochDuration,
    uint256 _emissionCap
) internal view returns (ProcessGaugeReturnValue memory returnData) {
    ...

    if (_gauge.incentive == IGaugeRegistrar.Incentive.Supply) {
        returnData.actionData = abi.encodeCall(
            IMultiRewardDistributor._updateSupplySpeed,
@>          (QiToken(_gauge.qiToken), rewardToken, newSpeed)
        );
    } else {
        returnData.actionData = abi.encodeCall(
            IMultiRewardDistributor._updateBorrowSpeed,
@>          (QiToken(_gauge.qiToken), rewardToken, newSpeed)
        );
    }
}
```

However, `MultiRewardDistributor` supports multiple reward tokens per `qiToken` market:

```solidity
/// @notice The main data storage for this contract, holds a mapping of qiToken to array
//          of market configs
mapping(address => MarketEmissionConfig[]) public marketConfigs;
```

> Each market has an array of configs, each with a unique emission token owned by a specific team/user. That owner can adjust supply and borrow emissions, end times, and ...

This can also be observed in the logic of `_updateSupplySpeed()` and `_updateBorrowSpeed()`, which are the calls encoded within the `BenqiEcosystemModule`:

```solidity
    function _updateSupplySpeed(
        QiToken _qiToken,
        address _emissionToken,
        uint256 _newSupplySpeed
    ) external onlyEmissionConfigOwnerOrAdmin(_qiToken, _emissionToken) {
        MarketEmissionConfig storage emissionConfig = fetchConfigByEmissionToken(
@>          _qiToken,
@>          _emissionToken
        );
        ...
    }
```

```solidity
function fetchConfigByEmissionToken(
    QiToken _qiToken,
    address _emissionToken
) internal view returns (MarketEmissionConfig storage) {
    MarketEmissionConfig[] storage configs = marketConfigs[address(_qiToken)];
    for (uint256 index = 0; index < configs.length; index++) {
        MarketEmissionConfig storage emissionConfig = configs[index];
        if (emissionConfig.config.emissionToken == _emissionToken) {
            return emissionConfig;
        }
    }

    revert("Unable to find emission token in qiToken configs");
}
```

**Impact:** The `BenqiEcosystemModule` can only adjust the speed for whichever single token was set in the constructor. It cannot differentiate or control the other emission tokens, even though they can exist and be active in the `MultiRewardDistributor`.

**Recommended Mitigation:** Consider allowing the `BenqiEcosystemModule` and the `Distributor` to pass different reward tokens.

**BENQI:** Acknowledged, this is purely a QI distributor.

**Cyfrin:** Acknowledged.
