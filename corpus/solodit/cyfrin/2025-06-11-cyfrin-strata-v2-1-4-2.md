---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Use named returns where this can eliminate in-function variable declaration
vuln_class: []
---

# Use named returns where this can eliminate in-function variable declaration

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Use named returns where this can eliminate in-function variable declaration:

* `yUSDeVault` : functions `totalAccruedUSDe`, `_convertAssetsToUSDe`, `previewDeposit`, `previewMint`
* `pUSDeVault` : function `previewYield`
* `MetaVault` : functions `deposit`, `mint`, `withdraw`, `redeem`

**Strata:** Fixed in commits [3241635](https://github.com/Strata-Money/contracts/commit/32416357ac166b072e4339471107e40950952a08) and [c68a705](https://github.com/Strata-Money/contracts/commit/c68a7053097a1909c13c98b6a5678a102f3f5007).

**Cyfrin:** Verified.
