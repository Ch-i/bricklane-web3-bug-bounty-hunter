---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Missing check for `validatorMEVRewardsPercentage` in `PolygonStrategy::initialize`
vuln_class: []
---

# Missing check for `validatorMEVRewardsPercentage` in `PolygonStrategy::initialize`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** `validatorMEVRewardsPercentage`is a reward percentage with valid values ranging from 0 to 10000 (100%). `PolygonStrategy::setValidatorMEVRewardsPercentage` rightly checks that the reward percentage does not exceed 10000. However this validation is missing during initialization.

```solidity
    function initialize(
        address _token,
        address _stakingPool,
        address _stakeManager,
        address _vaultImplementation,
        uint256 _validatorMEVRewardsPercentage,
        Fee[] memory _fees
    ) public initializer {
        __Strategy_init(_token, _stakingPool);

        stakeManager = _stakeManager;
        vaultImplementation = _vaultImplementation;
        validatorMEVRewardsPercentage = _validatorMEVRewardsPercentage; //@audit missing check on validatorMEVRewardsPercentage

```

**Recommended Mitigation:** Consider making the validation checks consistent at every place where the `validatorMEVRewardsPercentage` is updated.

**Stake.Link:** Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/2ef53d4f0dac80c6ba1dc31ec516a28d7ed02851)

**Cyfrin:** Resolved.
