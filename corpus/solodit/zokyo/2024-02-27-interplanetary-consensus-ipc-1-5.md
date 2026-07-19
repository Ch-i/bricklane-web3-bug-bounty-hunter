---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-1-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: '`SubnetKeys[]` Should Be Removed'
vuln_class: []
---

# `SubnetKeys[]` Should Be Removed

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Medium

**Status** - Resolved

**Description**


Inside the `kill()` function in the contract `GatewayManagerFacet.sol` , we decrease the `totalSubnets` at L135 , then delete `subnets[subnet.id.toHash()]` .  
Since `subnetKeys` array hold the keys of the registered subnets , `subnetKeys[subnet.id]` should also be removed when a subnet is killed.

**Recommendation**:

Along with `totalSubnets`  and `subnets[]` also update the `subnetKeys[]` when a subnet is killed
