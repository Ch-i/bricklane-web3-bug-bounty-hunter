---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Disabled operators can register new validator nodes
vuln_class: []
---

# Disabled operators can register new validator nodes

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `AvalancheL1Middleware::addNode` function allows an operator to register a new node if msg.sender is included in the operators list. However, there is a potential issue with how the operator lifecycle is handled: before an operator is permanently removed via removeOperator, it must first be placed into a "disabled" state using disableOperator.

The problem arises because the addNode function does not check whether the operator is in a disabled state—it only checks for existence in the operators set. As a result, a disabled operator  can still call addNode, even though operationally they are expected to be inactive during this period.

**Impact:** A disabled operator can continue to register new validator nodes via addNode, despite being in a state that should preclude them from performing such actions.

**Recommended Mitigation:** Update the addNode function to also check whether the operator is enabled, not just registered:

```diff
(, uint48 disabledTime) = operators.getTimes(operator);
+if (!operators.contains(operator) || disabledTime > 0 ) {
-if (!operators.contains(operator)) {
    revert AvalancheL1Middleware__OperatorNotActive(operator);
}
```
**Suzaku:**
Fixed in commit [0e0d4ae](https://github.com/suzaku-network/suzaku-core/pull/155/commits/0e0d4aee6394b8acbda391e107db8fb9f49f7102).

**Cyfrin:** Verified.
