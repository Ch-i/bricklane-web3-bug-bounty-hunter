---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Misleading revert message in onlyUser modifier
vuln_class: []
---

# Misleading revert message in onlyUser modifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** The `onlyUser` modifier restricts access by checking `msg.sender == user`, however the revert message uses "OnlyOwner", which is misleading since the restricted role is not an owner but a specific user address.

**Recommended Mitigation:** Update the revert message to accurately reflect the enforced role (e.g. "OnlyUser" or "Unauthorized")

**Strata:** Fixed in commit [b2ddea9](https://github.com/Strata-Money/contracts-tranches/commit/b2ddea94d22b1dc791ffada5d8afb32e8e2a579e).

**Cyfrin:** Verified.
