---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Use `immutable` for storage slots only set once in the constructor of non-upgradeable
  contracts
vuln_class: []
---

# Use `immutable` for storage slots only set once in the constructor of non-upgradeable contracts

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** Use `immutable` for storage slots only set once in the constructor:
* `MTokenMessager::ccipClient`
* `MTokenMessagerBase::ccipClient`

**Matrixdock:** Fixed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b#diff-dab651c3b43b10cc975bd594f600387ed27d1bffd16250f576c85820925fab9aR6-L8) for `MTokenMessagerBase`.

**Cyfrin:** Verified.
