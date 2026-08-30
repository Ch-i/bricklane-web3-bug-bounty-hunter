---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`IBTCY::approve` is blocked while paused, preventing users from revoking allowances
  during emergencies'
vuln_class: []
---

# `IBTCY::approve` is blocked while paused, preventing users from revoking allowances during emergencies

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCY::approve` has the `whenNotPaused` modifier. In a pause scenario, users cannot update allowances, including reducing them to zero to revoke previously granted approvals. Since transfers are already restricted under pause, allowing allowance updates during pause would not meaningfully expand token movement but would let users reduce exposure to compromised spenders.

**Impact:** During an incident (e.g., compromised spender/contract), pausing the token prevents users from revoking approvals, leaving existing allowances in place until unpaused and increasing risk if/when the token is later unpaused or if any allowance-based pathway remains usable.

**Recommended Mitigation:** Consider removing the `whenNotPaused` restriction from `approve`.

**Aarc:** Fixed in commit [e52faa9](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/e52faa9222a79973f12d8c8bb3273e9e385e21e5).

**Cyfrin:** Verified.
