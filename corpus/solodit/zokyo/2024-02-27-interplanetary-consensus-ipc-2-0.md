---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-2-0
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
title: Fee For Funding A Subnet Is Hardcoded To 0
vuln_class: []
---

# Fee For Funding A Subnet Is Hardcoded To 0

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Low

**Status** - Acknowledged

**Description**

It is currently decided that funding a subnet is free , but according to the comment at L144 GatewayManagerFacet.sol “There may be an associated fee that gets distributed to validators”

But the fee is hardcoded to 0 at L170

**Recommendation**: Instead of hardcoding the fee have a setter which sets the fee used depending on the decision.

**Client comment**: Accepted. We are going to remove the Funding mechanism. That will fix this and several critical issues. It will be redesigned and implemented later. The issues with low/info severity are tracked here - https://github.com/consensus-shipyard/ipc/issues/536
