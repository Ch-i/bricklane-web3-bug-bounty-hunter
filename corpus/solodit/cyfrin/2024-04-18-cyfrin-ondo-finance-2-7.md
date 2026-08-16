---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Remove return parameters from `rOUSG::_mintShares` and `_burnShares` as they
  are never read
vuln_class: []
---

# Remove return parameters from `rOUSG::_mintShares` and `_burnShares` as they are never read

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** Remove return parameters from `rOUSG::_mintShares` and `_burnShares` as they are never read. This saves 1 storage read in each function plus the cost of the return parameters.

**Ondo:**
Fixed in commit [dc91728](https://github.com/ondoprotocol/rwa-internal/commit/dc91728630a47ba351150287e48547a405a1282e).

**Cyfrin:** Verified.
