---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: External call is fed the wrong `QuorumObjKind` Parameter
vuln_class: []
---

# External call is fed the wrong `QuorumObjKind` Parameter

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

GatewayRouterFacet.sol - In `execBottomUpMsgBatch` function, the kind argument for `distributeRewardToRelayers` (i.e. in the encodeCall) should be `QuoromObjKind.BottomUpMsgBatch` instead of `QuoromObjKind.Checkpoint`.
```solidity
Address.functionCallWithValue({
    target: msg.sender,
    data: abi.encodeCall(
        ISubnetActor.distributeRewardToRelayers,
        (block.number, totalFee, QuorumObjKind.Checkpoint)
    ),
    value: totalFee
});
```
The issue is limited though by the fact that this feature is not yet implemented in SubnetActorManagerFacet as shown here:
```solidity
       } else if (kind == QuorumObjKind.BottomUpMsgBatch) {
            // FIXME: The distribution of rewards for batches can't be done
            // as for checkpoints (due to how they are submitted). As
            // we are running out of time, we'll defer this for the future.
            revert MethodNotAllowed("rewards not defined for batches");
        }
```
But for customly implemented subnets that can pose a serious issue if the implemented subnet is not aware about the lack of this feature.
**Recommendation** 

Apply the correct kind in encodeCall or reject that transaction the GatewayRouterFacet as well since the feature is not enabled yet.
**Fix**: That part is removed as of commit 4a2acb6  hence making the issue no longer relevant.
