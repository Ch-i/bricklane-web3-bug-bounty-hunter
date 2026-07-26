---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-0-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Vulnerability in `kill()` Function Allowing Premature Disruption in `SubnetActorManagerFacet`
vuln_class: []
---

# Vulnerability in `kill()` Function Allowing Premature Disruption in `SubnetActorManagerFacet`

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: High

**Status**: Resolved 

**Location**: SubnetActorManagerFacet.sol

**Description**

The `kill()` function in the `SubnetActorManagerFacet` contract, which is designed to deactivate the subnet when all validators have left, contains a significant vulnerability. The function can be called by any external actor, and when executed, it essentially disables most of the subnet's functionality. This is due to the widespread use of the `notKilled` modifier in various functions within the contract. A critical issue arises at the initial deployment phase of the `SubnetActorManagerFacet`, as it starts without any validators. This allows a potential attacker (griefer) to monitor new contract deployments and call the `kill()` function before any validators are added. This action renders the newly deployed contract useless. If executed on a large scale, this vulnerability can severely disrupt the deployment and operation of subnets within the system.
This flaw can be used to launch a denial-of-service attack against the network, preventing the effective use and deployment of new subnets 
**Recommendation**:  

Allow `kill()` to be callable after a prespecified time has passed after deployment.
