---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-12
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`RevenueCounter::initialize` missing zero-owner check'
vuln_class: []
---

# `RevenueCounter::initialize` missing zero-owner check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `RevenueCounter::initialize` does not assert `_owner != address(0)`.

**Impact:** A misdeploy that passes zero leaves the contract ungovernable.

**Recommended Mitigation:** Add `require(_owner != address(0))` at the top of `initialize`.

**Armada:** Fixed in commit [6cb5376](https://github.com/ship-armada/armada-poc/commit/6cb5376d1d127357b484ed9d6f0f8720450bc46f).

**Cyfrin:** Verified.
