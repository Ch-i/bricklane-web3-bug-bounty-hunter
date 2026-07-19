---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Consider using a 2-step process to change `governor` in `ChainlinkOracle`
vuln_class: []
---

# Consider using a 2-step process to change `governor` in `ChainlinkOracle`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** `ChainlinkOracleConfigs::updateGovernor` switches `governor` in a single call. A typo or compromised signer could irreversibly hand over control. Consider using a 2-step process for `governor` changes as is done in `Licredity` (`RiskConfig`)

**Licredity:** Fixed in [PR#19](https://github.com/Licredity/licredity-v1-oracle/pull/19/files), commit [`716cd8d`](https://github.com/Licredity/licredity-v1-oracle/commit/716cd8d269ef4149a8121e25affcc97ef416018a).

**Cyfrin:** Verified. 2stop governor handover is now used.
