---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`ChainlinkAdapter::_constructPayouts` silent `[0,0]` fallthrough on unexpected
  outcome'
vuln_class: []
---

# `ChainlinkAdapter::_constructPayouts` silent `[0,0]` fallthrough on unexpected outcome

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ChainlinkAdapter::_constructPayouts` uses `if / else if / else if` without a default. An unexpected price input silently returns `[0,0]` -> CTF locks funds (no payout for anyone). Not reachable today.

**Impact:** If a future refactor introduces an unhandled outcome path, funds lock in CTF with no payout.

**Recommended Mitigation:** Add an explicit `else revert ChainlinkAdapter__InvalidOutcome(price);` default branch.

**Predict.fun:** Fixed in commit [54942ac](https://github.com/PredictDotFun/prediction-market/commit/54942acc17044c2764fdecbf24a35c06c8091389).

**Cyfrin:** Verified.
