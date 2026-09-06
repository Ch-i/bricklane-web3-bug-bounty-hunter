---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Missing bounty percentage and cap validation
vuln_class: []
---

# Missing bounty percentage and cap validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** The `Agreement::_validateBountyTerms` lacks two important validations:

1. No upper bound is enforced on `bountyPercentage`
2.  No validation that `aggregateBountyCapUSD >= bountyCapUSD`


**Impact:** If `bountyPercentage > 100` is set mistakenly by the owner, protocol can become legally liable to pay more than what was recovered when `retainable = false`.

`aggregateBountyCapUSD >= bountyCapUSD` also creates ambiguity that can lead to disputes. For eg., If `bountyCapUSD = $1M` but `aggregateBountyCapUSD = $500K`, it's unclear whether a single whitehat can receive $1M or is limited to $500K.

**Recommended Mitigation:** Consider adding additional validations to `Agreement::_validateBountyTerms`.

**SafeHarbor:**
Fixed in [3c0b5a95](https://github.com/PatrickAlphaC/safe-harbor/commit/3c0b5a95c926e716fae2aada8ef6070dd6da019a).

**Cyfrin:** Verified.
