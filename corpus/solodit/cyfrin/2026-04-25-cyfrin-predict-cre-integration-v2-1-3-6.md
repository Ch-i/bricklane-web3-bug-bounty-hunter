---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-3-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`ChainlinkReceiverBase::onReport` storage re-reads of optional permission
  fields'
vuln_class: []
---

# `ChainlinkReceiverBase::onReport` storage re-reads of optional permission fields

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ChainlinkReceiverBase::onReport` reads `s_expectedAuthor` up to 3 times on the success path and `s_expectedWorkflowName` up to 2 times. Warm SLOADs (~100 gas each) but caching clarifies control flow. Overlaps with the G-3 issue.

**Impact:** Minor warm-SLOAD gas waste; modest readability hit.

**Recommended Mitigation:**
```solidity
address expectedAuthor = s_expectedAuthor;
bytes10 expectedName = s_expectedWorkflowName;
if (expectedAuthor != address(0) || expectedName != bytes10(0)) {
    if (expectedAuthor != address(0) && workflowOwner != expectedAuthor) revert InvalidAuthor(workflowOwner, expectedAuthor);
    if (expectedName != bytes10(0)) {
        if (expectedAuthor == address(0)) revert WorkflowNameRequiresAuthorValidation();
        if (workflowName != expectedName) revert InvalidWorkflowName(workflowName, expectedName);
    }
}
```

**Predict.fun:** Fixed in commit [a0aa366](https://github.com/PredictDotFun/prediction-market/commit/a0aa3660fef0f8f08806db61d48a0a4ec8fd1cca) which:
* refactored `s_expectedAuthor` and `s_expectedWorkflowName` into a mapping and now set in `setIsWorkflowAuthorAndNameValid`
* in `onReport` replaced the previous code with `if (!isWorkflowAuthorAndNameValid[workflowOwner][workflowName])` that reads the owner workflow and name once

**Cyfrin:** Verified.

\clearpage
