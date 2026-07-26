---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Input lack validation to be non-zero
vuln_class: []
---

# Input lack validation to be non-zero

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

LibGateway.sol - In `storeBottomUpCheckpoint` function, the input checkpoint is not being validated. It accepts a zero value of checkpoint.blockHeight. Note that if blockHeight is zero it implies the non-existence of a checkpoint to begin with.
```solidity
   function storeBottomUpCheckpoint(
        BottomUpCheckpoint memory checkpoint
    ) internal {
        GatewayActorStorage storage s = LibGatewayActorStorage.appStorage();
        s.bottomUpCheckpoints[checkpoint.blockHeight] = checkpoint;
    }
```
That library method is being used in GatewayRouterFacet as follow:
```solidity
   function createBottomUpCheckpoint(
        BottomUpCheckpoint calldata checkpoint,
        bytes32 membershipRootHash,
        uint256 membershipWeight
    ) external systemActorOnly {
        if (checkpoint.blockHeight % s.bottomUpCheckPeriod != 0) {
            revert InvalidCheckpointEpoch();
        }
        if (LibGateway.bottomUpCheckpointExists(checkpoint.blockHeight)) {
            revert CheckpointAlreadyExists();
        }

        LibQuorum.createQuorumInfo({
            self: s.checkpointQuorumMap,
            objHeight: checkpoint.blockHeight,
            objHash: keccak256(abi.encode(checkpoint)),
            membershipRootHash: membershipRootHash,
            membershipWeight: membershipWeight,
            majorityPercentage: s.majorityPercentage
        });
        LibGateway.storeBottomUpCheckpoint(checkpoint);
    }
```
This shows that `checkpoint.blockHeight` can pass through with a zero value: `if (checkpoint.blockHeight % s.bottomUpCheckPeriod != 0)`. But the issue is limited because of `systemActorOnly` modifier which limits the access of this function.

**Recommendation**

Apply the necessary input validation.
