---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Consider renaming `MTokenMessagerBase::ccipClient` as it is used by LayerZero
  integration and actually refers to `MToken`
vuln_class: []
---

# Consider renaming `MTokenMessagerBase::ccipClient` as it is used by LayerZero integration and actually refers to `MToken`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** `MTokenMessager::ccipClient` and `MTokenMessagerBase::ccipClient` are used by both LayerZero (`MTokenMessagerLZ`) and CCIP (MTokenMessagerV2`).

But they actually simply reference the `MToken` contract. Calling them `ccipClient` is initially confusing especially when reading the LayerZero integration and wondering why it is calling `ccipClient`.

Consider renaming `MTokenMessager::ccipClient` and `MTokenMessagerBase::ccipClient` to `mToken` and simply adding the additional functions to `IMToken` then deleting `ICCIPClient`.

**Matrixdock:** Fixed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b#diff-dab651c3b43b10cc975bd594f600387ed27d1bffd16250f576c85820925fab9aR6-R9) for `MTokenMessagerBase`.

**Cyfrin:** Verified.
