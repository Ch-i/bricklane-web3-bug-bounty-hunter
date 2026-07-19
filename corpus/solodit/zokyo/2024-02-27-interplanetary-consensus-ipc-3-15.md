---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-15
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Code Behaves Differently From The Comment
vuln_class: []
---

# Code Behaves Differently From The Comment

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Informational

**Status** - Resolved

**Description**

The comment at L248 in `SubnetActorManagerFacet` says “adding this check to prevent new validators from joining after the subnet has been bootstrapped”  ,  but the check ,
```solidity
if (s.bootstrapped) {
            enforceCollateralValidation();
        }
```
Does not enforce this, validators still can join with the condition that collateral validation is enforced.

Recommendation: Update the comment or the code
