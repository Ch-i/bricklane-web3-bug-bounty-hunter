---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`setExpectedAuthor(address(0))` with non-empty workflow name causes `onReport`
  DoS'
vuln_class: []
---

# `setExpectedAuthor(address(0))` with non-empty workflow name causes `onReport` DoS

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Order-independent setters on `ChainlinkReceiverBase` skip the "name requires author" invariant at config time. One admin mis-step (setting author to zero while name is non-empty via `setExpectedAuthor(address(0))`) bricks settlement via the runtime check at `ChainlinkReceiverBase.sol:112`.

**Impact:** A single admin misconfiguration triggers a full `onReport` DoS — settlement is blocked until the admin reverses the change.

**Recommended Mitigation:** In `setExpectedAuthor`, revert if `_author == address(0) && s_expectedWorkflowName != bytes10(0)`. Fails fast at config time instead of at every `onReport`.

**Predict.fun:** Fixed in commit [a0aa366](https://github.com/PredictDotFun/prediction-market/pull/71/changes/a0aa3660fef0f8f08806db61d48a0a4ec8fd1cca).

**Cyfrin:** Verified.
