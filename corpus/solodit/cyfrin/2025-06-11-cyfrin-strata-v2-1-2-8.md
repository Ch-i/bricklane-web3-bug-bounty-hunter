---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: No way to compound deposited supported vault assets into `sUSDe` stake during
  yield phase
vuln_class: []
---

# No way to compound deposited supported vault assets into `sUSDe` stake during yield phase

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Once the yield phase has been enabled, `pUSDeVault` still allows new supported vaults to be added and deposits via supported vaults.

However for supported vaults which are not `sUSDe`, there is no way to withdraw their base token `USDe` and compound into the `sUSDe` vault stake used by the `pUSDeVault` vault.

**Recommended Mitigation:** Either don't allow supported vaults to be added apart from `sUSDe` once yield phase has been enabled, or implement a function to withdraw their base token and compound it into the main stake.

**Strata:** Fixed in commit [076d23e](https://github.com/Strata-Money/contracts/commit/076d23e2446ad6780b2c014d66a46e54425a8769#diff-34cf784187ffa876f573d51b705940947bc06ec85f8c303c1b16a4759f59524eR190) by no longer allowing adding new supporting vaults during the yield phase.

**Cyfrin:** Verified.
