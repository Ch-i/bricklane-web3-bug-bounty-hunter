---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Inline small internal functions only used once
vuln_class: []
---

# Inline small internal functions only used once

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** It is more gas efficient to inline small internal functions only used once.

For example `pUSDeDepositor::getPhase` is only called by `deposit_sUSDe`. Changing `deposit_sUSDe` to cache `pUSDe` then use the cached copy in the call to `PreDepositPhaser::currentPhase` saves 1 storage read in addition to saving the function call overhead.

**Strata:** Fixed in commit [9398379](https://github.com/Strata-Money/contracts/commit/93983791adbd45a555d947a12a5a6fd9bbfe7330).

**Cyfrin:** Verified.
