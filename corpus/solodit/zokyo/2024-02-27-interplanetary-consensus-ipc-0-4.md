---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-0-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Reward Distribution Mechanism in `submitCheckpoint` Function can be gamed
vuln_class: []
---

# Reward Distribution Mechanism in `submitCheckpoint` Function can be gamed

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: High

**Status**: Acknowledged

**Location**: SubnetActorManagerFacet.sol

**Description**

The current implementation of the `submitCheckpoint` function in the contract allows for potential gaming of the reward system by validators. A significant loophole exists where a relayer can receive rewards even when submitting a checkpoint late. This opens up a scenario where a relayer can listen to other relayers' submissions and submit within the same epoch, potentially even front-running these transactions. This behavior leads to the dilution of fee distribution, as more relayers share the fees, thereby reducing the intended rewards for timely and legitimate submissions.
**Implications**:
Dilution of Rewards: Genuine relayers who submit checkpoints promptly might receive lower rewards due to the increased number of participants in the reward pool, including those who submit late.
Incentive Misalignment: This issue could lead to a scenario where relayers are incentivized to wait and copy other submissions rather than participating in a timely and honest manner.
Potential for Manipulation: Malicious actors could exploit this vulnerability to consistently gain rewards without contributing meaningful work.

**Recommendation** :

Implement Commit-Reveal Scheme: Redesign the reward mechanism using a commit-reveal scheme. In this approach, relayers would first commit to a checkpoint without revealing their identity or submission details. After a designated commit period, a separate reveal phase would allow relayers to disclose their submissions. This method can prevent front-running and copying of submissions. This is a suggestion, there may be other approaches more appropriate for this protocol.
