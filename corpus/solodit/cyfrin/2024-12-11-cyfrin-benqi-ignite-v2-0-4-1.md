---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-4-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Unnecessary validation in `StakingContract::registerNode`
vuln_class: []
---

# Unnecessary validation in `StakingContract::registerNode`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** When a new validator node has been created on behalf of a user, the Zeeve admin reports this by calling `StakingContract::registerNode` which performs some validation before invoking `Ignite::registerWithPrevalidatedQiStake` to register the node according to the requirements in `Ignite`.

Some of this validation done in `StakingContract::registerNode`, shown below, is unnecessary and can be removed.

```solidity
require(
    bytes(nodeId).length > 0 && blsProofOfPossession.length > 0,
    "Invalid node or BLS key"
);
require(
    igniteContract.registrationIndicesByNodeId(nodeId) == 0,
    "Node ID already registered"
);
```

All of [this validation](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L406-413) around `nodeId`, `blsProofOfPossesion`, and the registration index is [performed again](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L973-L979) in `Ignite::_register`.

```solidity
// Retrieve the staking details from the stored records
require(stakeRecords[user].stakeCount > 0, "Staking details not found");
require(index < stakeRecords[user].stakeCount, "Index out of bounds"); // Ensures the index is valid

StakeRecord storage record = stakeRecords[user].records[index]; // Access the record by index
```

If [these requirements](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L414-416) were removed, an invalid index or zero stake count would result in an uninitialized `StakeRecord being [returned](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L418). Thus, execution would revert on all of the subsequent requirements:

```solidity
require(record.timestamp != 0, "Staking details not found");
require(isValidDuration(record.duration), "Invalid duration");
// Ensure the staking status is Provisioning
require(
    record.status == StakingStatus.Provisioning,
    "Invalid staking status"
);
```

Even still, the [timestamp validation](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L419) is superfluous as there is no way for an existing record to have an uninitialized `timestamp`, and the record is guaranteed to exist by the subsequent check on [`status`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L422-425). This means that the [`duration`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L420) validation is also unnecessary, as it is not needed to guarantee the existence of a record and is performed again in [`Ignite::_regiserWithChecks`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L930-L936).

**Recommended Mitigation:** Consider removing the unnecessary validation outlined above.

**BENQI:** Acknowledged. Kept as a redundancy check.

**Cyfrin:** Acknowledged.
