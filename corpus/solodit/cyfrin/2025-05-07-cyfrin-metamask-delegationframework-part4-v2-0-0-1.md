---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-07-cyfrin-metamask-delegationframework-part4-v2-0-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-05-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-07-cyfrin-metamask-delegationFramework-part4-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-07-cyfrin-metamask-delegationframework-part4-v2-0
title: Delegate controlled privilege escalation risk in `LogicalOrWrapperEnforcer`
vuln_class: []
---

# Delegate controlled privilege escalation risk in `LogicalOrWrapperEnforcer`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-07-cyfrin-metamask-delegationFramework-part4-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-07-cyfrin-metamask-delegationFramework-part4-v2.0.md)_

---

**Description:** When using the `LogicalOrWrapperEnforcer` enforcer, delegators may define multiple caveat groups with different security properties, expecting that all groups provide adequate security boundaries.

However, since delegates control which group is evaluated during execution, they can select the least restrictive group to bypass stricter security requirements defined in other groups.

For example, if a delegator defines two groups:

- Group 0: Requires minimum balance change of 100 tokens
- Group 1: Requires minimum balance change of 50 tokens

A delegate can choose Group 1 at execution time, allowing them to transfer only 50 tokens when the delegator may have expected the 100 token minimum to apply.

While this behavior is by design, it creates a scenario where delegates can bypass intended security restrictions by selecting the least restrictive caveat group. Since this enforcer's behavior gives such control to the delegate, it effectively allows them to elevate their privileges to the least restrictive option available across all defined groups.

**Recommended Mitigation:** Consider adding a security notice similar to the one added in all balance change enforcers.

```solidity
/**
 * @dev Security Notice: This enforcer allows delegates to choose which caveat group to use at execution time
 * via the groupIndex parameter. If multiple caveat groups are defined with varying levels of restrictions,
 * delegates can select the least restrictive group, bypassing stricter requirements in other groups.
 *
 * To maintain proper security:
 * 1. Ensure each caveat group represents a complete and equally secure permission set
 * 2. Never assume delegates will select the most restrictive group
 * 3. Design caveat groups with the understanding that delegates will choose the path of least resistance
 *
 * Use this enforcer at your own risk and ensure it aligns with your intended security model.
 */
```


**Metamask:** Fixed in commit [d38d53d](https://github.com/MetaMask/delegation-framework/commit/d38d53dc467cc3b4faa7047cfca1844ea9cbc3be).

**Cyfrin:** Resolved.


\clearpage
