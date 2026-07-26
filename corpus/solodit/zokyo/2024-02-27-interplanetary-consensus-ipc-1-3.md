---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Use < Instead of <=
vuln_class: []
---

# Use < Instead of <=

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Medium

**Status** - Resolved

**Description**

Case 1:

In the function createBottomUpMsgBatch (L353 in GatewayRouterFacet.sol) we check that if we are trying to create a batch from the future and the check for that is ->
```solidity
if (batch.blockHeight % s.bottomUpMsgBatchPeriod != 0 || block.number <= batch.blockHeight) {
            revert InvalidBatchEpoch();        }
```
This check would make the code revert even if `block.number == batch.blockHeight` which is not a block from the future but the current block.

Case 2:

In the `register()` function (GatewayManagerFacet.sol L32) ,it is checked that route length after the addition of the subnet i.e. `route.length + 1` must not exceed `maxTreeDepth`.
```solidity
if (s.networkName.route.length + 1 >= s.maxTreeDepth) {
            revert MethodNotAllowed(ERR_CHILD_SUBNET_NOT_ALLOWED);
        }
```
But this condition would revert even when new length after addition is equal to `maxTreeDepth` while the value `maxTreeDepth` should be allowed . 


**Recommendation**:

Change the statement to 
```solidity
if (batch.blockHeight % s.bottomUpMsgBatchPeriod != 0 || block.number < batch.blockHeight) {
            revert InvalidBatchEpoch();
        }
```
And  , 
```solidity
if (s.networkName.route.length + 1 > s.maxTreeDepth) {
            revert MethodNotAllowed(ERR_CHILD_SUBNET_NOT_ALLOWED);
        }
```
