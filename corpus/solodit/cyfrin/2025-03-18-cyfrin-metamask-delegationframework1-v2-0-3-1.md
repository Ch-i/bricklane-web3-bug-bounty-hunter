---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: '`NotSelf()` error declaration is unused'
vuln_class: []
---

# `NotSelf()` error declaration is unused

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** The `DeleGatorCore` contract and `EIP7702DeleGatorCore` contract both define a custom error called `NotSelf()`, but this error is never actually thrown anywhere in either contract or their derived implementations.

```solidity
   // DeleGatorCore and EIP7702DeleGatorcore
    /// @dev Error thrown when the caller is not this contract.
    error NotSelf();
```

**Recommended Mitigation:** Consider removing the error from these two contracts

**Metamask:** Acknowledged. Will keep this incase inheriting implementations wish to leverage in the future.

**Cyfrin:** Acknowledged.
