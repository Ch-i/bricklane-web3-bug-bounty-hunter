---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Missing runtime input validation in admin setters and extension paths
vuln_class: []
---

# Missing runtime input validation in admin setters and extension paths

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Grouping of runtime missing-input-validation findings in admin setters and extension paths on `ChainlinkUpDownAdapter` and `ChainlinkReceiverBase`. All are admin-gated but each lets an admin typo or misconfiguration produce a runtime fault the contract should have rejected at function entry.

---

**1. `ChainlinkUpDownAdapter::initialize, extend, enableRoundConfig` accept unbounded `roundCount`**

`roundCount` is unbounded in all three functions. An admin or extender typo causes out-of-gas on the creation transaction. Role-gated and bounded in practice, but the contract offers no defensive ceiling.

**Impact:** Out-of-gas on the creation transaction; transaction wasted, no state corruption.

**Recommended:** `if (roundCount > MAX_ROUND_COUNT) revert ...;` with `MAX_ROUND_COUNT` chosen such that `gas x MAX_ROUND_COUNT` stays under ~80% of the BSC block gas limit.


**2. `ChainlinkReceiverBase::setIsWorkflowIdValid(bytes32(0), true)` accepted**

An admin typo or badly-encoded metadata could enable a zero`workflowId`, opening the gate for any caller whose metadata encodes a zero workflow id.

**Impact:** Admin misconfiguration could disable workflow-id validation entirely, allowing any caller metadata encoding a zero workflow id to pass the gate.

**Recommended:** Reject `workflowId == bytes32(0)` in `setIsWorkflowIdValid`:

```solidity
if (workflowId == bytes32(0)) revert InvalidWorkflowId();
```

---

**Predict.fun:** Fixed in commit [981b4a4](https://github.com/PredictDotFun/prediction-market/pull/71/commits/981b4a461712e74482ab74c1945c38d48467a1ff).

**Cyfrin:** Verified.
