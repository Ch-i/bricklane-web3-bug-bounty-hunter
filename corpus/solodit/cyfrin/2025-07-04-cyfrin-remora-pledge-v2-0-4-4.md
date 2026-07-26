---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Variables in non-upgradeable contracts which are only set once in `constructor`
  should be declared `immutable`
vuln_class: []
---

# Variables in non-upgradeable contracts which are only set once in `constructor` should be declared `immutable`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Variables in non-upgradeable contracts which are only set once in `constructor` should be declared `immutable`:
* `PledgeManager::holderWallet`, `propertyToken`, `stablecoin`, `stablecoinDecimals`, `deadline`, `postDeadlineWithdrawPeriod`, `pricePerToken`

**Remora:** Fixed in commit [afd07fb](https://github.com/remora-projects/remora-smart-contracts/commit/afd07fb419c354dc223d0105b2fd0c5d565f465f).

**Cyfrin:** Verified.
