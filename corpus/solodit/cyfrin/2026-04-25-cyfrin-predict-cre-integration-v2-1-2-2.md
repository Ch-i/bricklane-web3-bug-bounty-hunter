---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Missing `whenNotPaused` on `onReport` pre-validation and no reentrancy guards
  on CTF calls
vuln_class: []
---

# Missing `whenNotPaused` on `onReport` pre-validation and no reentrancy guards on CTF calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Pause semantics are inconsistent in `ChainlinkReceiverBase::onReport` — metadata validation runs even when paused (though `_processReport` itself is guarded by `whenNotPaused`). CTF and VerifierProxy are trusted integrations, so the reentrancy surface is bounded.

**Impact:** During pause, metadata validation still runs (gas waste) before the inner `whenNotPaused` reverts. No direct fund impact because CTF / VerifierProxy are trusted, but defensive reentrancy coverage is missing.

**Recommended Mitigation:** Move `whenNotPaused` to the top of `onReport` so pre-validation short-circuits under pause. Add OZ `ReentrancyGuard` on `onReport` defensively.

**Predict.fun:** Acknowledged; `ChainlinkReceiverBase` is a copy of Chainlink's `ReceiverTemplate` so we tried to make as few changes to the base contract as possible. As there are no demonstrated security issues we'd prefer not to make any additional changes to this contract.
