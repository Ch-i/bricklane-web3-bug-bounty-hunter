---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Remove event parameters that always have the same value
vuln_class: []
---

# Remove event parameters that always have the same value

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Remove event parameters that always have the same value:
* `MintRequested::feesInBTC` - always zero (see `IBTCYHub::requestSubscription`)

**Aarc:** Fixed in commit [7244f81](https://github.com/aarc-xyz/btcy-contracts-main/commit/7244f8111abca14e9f4e68253634af64b44a396e).

**Cyfrin:** Verified.
