---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-4-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Variables only set once in `constructor` of non-upgradeable contracts should
  be declared `immutable`
vuln_class: []
---

# Variables only set once in `constructor` of non-upgradeable contracts should be declared `immutable`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Variables only set once in `constructor` of non-upgradeable contracts should be declared `immutable`:
* `CompliantDepositRegistry::complianceChecker`
* `Minter::baseAsset, hilBTCToken`

**Syntetika:**
Fixed in commit [3d1e596](https://github.com/SyntetikaLabs/monorepo/commit/3d1e5967e99de56cb212565eca42845ba8149784).

**Cyfrin:** Verified.
