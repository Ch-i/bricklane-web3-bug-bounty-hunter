---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`IBTCY::processSubscriptions` doesn''t revert when `subscriptionPaused ==
  true`'
vuln_class: []
---

# `IBTCY::processSubscriptions` doesn't revert when `subscriptionPaused == true`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCY::processSubscriptions` doesn't revert when `subscriptionPaused == true`. This appears to be an oversight since its sister-function `processRedemptions` reverts when `redemptionPaused == true`.

**Aarc:** Fixed in commit [c129022](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/c129022860cfb5a85ed918fac9da89705df3e5ba).

**Cyfrin:** Verified.
