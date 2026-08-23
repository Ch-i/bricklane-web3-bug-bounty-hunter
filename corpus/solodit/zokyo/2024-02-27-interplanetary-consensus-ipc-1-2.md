---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Marked active despite not having enough collateral
vuln_class: []
---

# Marked active despite not having enough collateral

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

GatewayManagerFacet.sol - In `register()` function, collateral is not being validated to be greater than `s.minStake`. Consequently we end up having a subnet status marked as Status.Active as shown in the following:
```solidity
        subnet.id = subnetId;
        subnet.stake = collateral;
        subnet.status = Status.Active;
        subnet.genesisEpoch = block.number;
        subnet.circSupply = genesisCircSupply;
```
Noting that this contradicts the implementation of addStake function which asserts that the stake becomes greater than a given threshold (i.e. s.minStake) in order to have an active status as shown in the following:
```solidity
       if (subnet.status == Status.Inactive) {
            if (subnet.stake >= s.minStake) {
                subnet.status = Status.Active;
            }
        }
```
**Recommendation**

Apply the required validation method to ensure that collateral is the intended value to have an active subnet. 
**Fix**: Issue is fixed in commit 2440ac2 by removing   `subnet.status = Status.Active;`. Therefore the subnet is no longer marked active on calling register to avoid that mislabelling if collateral is not enough.
**Client comment**: Invalid. There is no such vulnerability in the latest codebase after implementing changes in the protocol - https://www.google.com/url?q=https://github.com/consensus-shipyard/ipc-monorepo/blob/main/contracts/src/subnet/SubnetActorManagerFacet.sol%23L107-L254&sa=D&source=docs&ust=1704927823490184&usg=AOvVaw3-GVrDm8nvR39T5f8sH0Xv
