---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-4-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Use named return variables
vuln_class: []
---

# Use named return variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** There are a number of instances where named return variables could be used to avoid unnecessary stack variable assignments, for example in `FeeHandler._tokenDistribution()`. Consider modifying this and other relevant functions to save gas.

**OctoDeFi:** Fixed in PR [\#22](https://github.com/octodefi/strategy-builder-plugin/pull/22).

**Cyfrin:** Verified. Name return variables are now used.
