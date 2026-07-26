---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: '`StakingVault::claimWithdraw` should revert if `assets` are zero'
vuln_class: []
---

# `StakingVault::claimWithdraw` should revert if `assets` are zero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `StakingVault::claimWithdraw` should revert if `assets` are zero.

**Syntetika:**
Fixed in commit [2fe18df](https://github.com/SyntetikaLabs/monorepo/commit/2fe18df4891810f3daea17777ba7e1d9d7c80d0f).

**Cyfrin:** Verified.
