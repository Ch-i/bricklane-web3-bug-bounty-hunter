---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Infinite loop in the `exitValidators()` prevents users from calling `requestUnstake()`
vuln_class: []
---

# Infinite loop in the `exitValidators()` prevents users from calling `requestUnstake()`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** When users call function `requestUnstake()` to request to unstake their ETH, the `CasimirManager` contract will calculate if the current expected withdrawable balance is enough to cover all the queued unstaking requests. If it is not enough, the function `exitValidators()` will be call to exit some active validators to have enough ETH to fulfill all the unstaking requests.

In the function `exitValidators()`, it will do a while loop through the `stakedValidatorIds` list. If it found an active validator, it will call the `ssvClusters` to exit this validator and also change the status from `ACTIVE` to `EXITING`. However, if the validator status is not `ACTIVE`, the loop `index` will not be updated as well, resulting in the loop keep running infinitely but not being able to reach the next validator in the `stakedValidatorIds` list.
```solidity
function exitValidators(uint256 count) private {
    uint256 index = 0;
    while (count > 0) {
        uint32 validatorId = stakedValidatorIds[index];
        Validator storage validator = validators[validatorId];

        // @audit if status != ACTIVE, count and index won't be updated => Infinite loop
        if (validator.status == ValidatorStatus.ACTIVE) {
            count--;
            index++;
            requestedExits++;
            validator.status = ValidatorStatus.EXITING;
            ssvClusters.exitValidator(validator.publicKey, validator.operatorIds);
            emit ValidatorExited(validatorId);
        }
    }
}
```

**Impact:**
- If the status of first validator in the `stakedValidatorIds` list is not active, the `requestUnstake()` function will consume the caller's entire gas limit and revert.

- Could also lead to griefing attacks where a small staker can delay unstake requests of a whale staker by front-running an unstake request. While `exitValidators` will run successfully the first time, it will revert due to infinite loop when called by whale staker

**Recommended Mitigation:** Consider updating `count` and `index` variables to ensure the loop will break in all scenarios.

**Casimir:**
Fixed in [2945695](https://github.com/casimirlabs/casimir-contracts/commit/29456956e383e48277d604ca54d8fd43d6f31d10)

**Cyfrin:** Verified.
