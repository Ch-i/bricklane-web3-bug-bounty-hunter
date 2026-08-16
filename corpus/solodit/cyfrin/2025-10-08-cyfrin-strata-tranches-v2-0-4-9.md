---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-9
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Cooldown contracts underreport the real balance of users because they only
  consider the balance of requests whose cooldown period is over
vuln_class: []
---

# Cooldown contracts underreport the real balance of users because they only consider the balance of requests whose cooldown period is over

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** Cooldown contracts underreport the real balance of users because not all active requests are accounted for; only those requests whose cooldown period has expired are considered part of a user's balance.

This implementation doesn't accurately show the actual information about the user's balance at all times, only until requests are finalized (cooldown period is over).

**Recommended Mitigation:** Consider refactoring the `balanceOf()` method to return all balances, including both available and locked balances.

**Strata:**
Fixed in commit [949cb4](https://github.com/Strata-Money/contracts-tranches/commit/949cb474579036655fc3da066d8c35e77443ffd4) and [1f82c6](https://github.com/Strata-Money/contracts-tranches/commit/1f82c6a456272fd40afcb8792b7b4b3d9c13da20) to return more detailed data about the active requests, such as `pending` and `claimable` amounts, based on the lock periods.

**Cyfrin:** Verified.
