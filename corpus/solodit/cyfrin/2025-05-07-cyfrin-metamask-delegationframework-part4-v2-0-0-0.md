---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-07-cyfrin-metamask-delegationframework-part4-v2-0-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-05-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-07-cyfrin-metamask-delegationFramework-part4-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-07-cyfrin-metamask-delegationframework-part4-v2-0
title: Execution mode restriction in `LogicalOrWrapperEnforcer` can be removed
vuln_class: []
---

# Execution mode restriction in `LogicalOrWrapperEnforcer` can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-07-cyfrin-metamask-delegationFramework-part4-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-07-cyfrin-metamask-delegationFramework-part4-v2.0.md)_

---

**Description:** The `LogicalOrWrapperEnforcer` contract currently includes the `onlyDefaultExecutionMode` modifier on all of its hook functions. This creates an unnecessary restriction since the individual enforcers being wrapped already apply their own execution mode restrictions. This design decision could limit the wrapper's flexibility and prevent it from working with caveats that might support non-default execution modes.


**Recommended Mitigation:** Consider removing the `onlyDefaultExecutionMode` modifier from all hook functions in the `LogicalOrWrapperEnforcer` and let the individual wrapped caveat enforcers handle their own execution mode restrictions.

Not only is this gas efficient, this change would also allow the `LogicalOrWrapperEnforcer` to be more flexible and forward-compatible with future caveats, while still maintaining the appropriate execution mode restrictions through the wrapped enforcer contracts themselves.

**Metamask:** Fixed in commit [d38d53d](https://github.com/MetaMask/delegation-framework/commit/d38d53dc467cc3b4faa7047cfca1844ea9cbc3be).

**Cyfrin:** Resolved.
