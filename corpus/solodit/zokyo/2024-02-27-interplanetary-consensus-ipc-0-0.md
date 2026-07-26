---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-0-0
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
title: Vulnerability in Reward Distribution Mechanism Allowing Fund Theft in SubnetActorManagerFacet.sol
vuln_class: []
---

# Vulnerability in Reward Distribution Mechanism Allowing Fund Theft in SubnetActorManagerFacet.sol

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Critical 

**Status**: Resolved

**Location**: SubnetActorManagerFacet.sol contract, distributeRewardToRelayers function

**Description**

A critical vulnerability exists in the IPC protocol's distributeRewardToRelayers function of the SubnetActorManagerFacet.sol contract. This vulnerability allows an attacker to drain funds from a subnet by exploiting a sequence of operations involving crafted messages and checkpointing.
**Attack Process**:
- Initial Requirement: The attacker must have been a rewarded relayer for a past checkpoint.
- Message Crafting: The attacker creates a custom message targeting the distributeRewardToRelayers function. This message is crafted to specify a height for reward eligibility and a large reward amount.
- Checkpoint Commitment: The commitBottomUpCheckpoint function in GatewayRouterFacet.sol is invoked, executing the attacker’s crafted message.
- Malicious Reward Execution: The distributeRewardToRelayers function is executed with the parameters set by the attacker, bypassing security checks due to its origin from the gateway (satisfying the onlyGateway modifier).
- Fund Drainage: The attacker sets a high reward amount in the crafted message, leading to an unauthorized distribution of subnet funds.
- 
**Vulnerability Details**:
  
In the GatewayRouterFacet, the commitBottomUpCheckpoint function triggers _applyMessages, which is also part of the applyCrossMessages function.
When a cross message (crossMsg) is executed, if crossMsg.message.to.rawAddress is set to SubnetActorManagerFacet and crossMsg.message.method to distributeRewardToRelayers, the attack unfolds.
The attacker manipulates crossMsg.message.params to set desired height and value parameters by encoding function parameter data, similar to an encoded call.
**Entry Point for Attack**: The attacker utilizes the IPC protocol to craft custom call data on functions like sendUserXnetMessage in GatewayMessengerFacet. This crafted message is then applied during checkpoint commitment, triggering the vulnerability.

**Recommendation**:

To enhance the security and integrity of the protocol, a crucial recommendation is to implement a restriction within the system that disallows the use of protocol contract addresses as target addresses when crafting messages. This measure aims to prevent potential exploits or manipulations that might arise from interactions with protocol contract addresses.
