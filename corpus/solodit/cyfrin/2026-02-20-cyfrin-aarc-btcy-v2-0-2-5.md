---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Consider automatic allowlist configuration when changing compliance, fee receiver
  addresse
vuln_class: []
---

# Consider automatic allowlist configuration when changing compliance, fee receiver addresse

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCY` has a compliance address which can effectively seize tokens; presumably it needs to also be able to transfer tokens once seized.

Since `IBTCY` inherits from `AllowList`, in `IBTCY::setComplianceAddress` consider:
* removing the only compliance address from `AllowList`, and potentially reverting if its balance of tokens is greater than zero
* adding the new compliance address to `AllowList`

This approach ensures that only the current compliance address is only ever allowed and old addresses don't retain permissions.

A similar improvement could be made to `BTCY::setFeeRecipient`.

**Aarc:** Acknowledged; keeping allowlist management separate by design for operational flexibility.
