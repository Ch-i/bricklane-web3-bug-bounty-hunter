---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-1-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: '`commitCheckpoint` Returns Execution Without Rewarding The Relayer'
vuln_class: []
---

# `commitCheckpoint` Returns Execution Without Rewarding The Relayer

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Medium

**Status** - Resolved

**Description**

Function `commitCheckpoint()` (L41 GatewayRouterFacet.sol) commits a verified checkpoint and rewards the relayer if `checkpointRelayerRewards` is set to true . But a value of 0 is sent to the function `distributeRewardsToRelayer` at L64  , this would just return execution and not reward the relayer.

**Recommendation**: 

Reward the relayer appropriately
