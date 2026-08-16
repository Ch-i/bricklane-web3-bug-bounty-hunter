---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-14
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: '`minValidator` Check Can Be Done Before To Save Gas'
vuln_class: []
---

# `minValidator` Check Can Be Done Before To Save Gas

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**

The check at L560 in SubnetActorManagerFacet.sol (to check if the length is less than minValidators) can be done on the beginning of the function preBootstrapSetFederatedPower , that way if the length is less than the minValidators then it does not need to go through the for loop.

 **Recommendation**:

Have the check at the beginning of the function.
