---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Unstaking rounds in favor of users
vuln_class: []
---

# Unstaking rounds in favor of users

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Unstaking via `StakeManager` computes the delta in the MP values based on the % unstaked by the user out of the total staked by him, using `mulDiv` which rounds down. Then, these values are used for subtracting. As higher MP values benefit the user, then subtracting less benefits him, thus the roundings were in favor of him.

**Impact:** Wrong roundings favor the user. The impact is not significant, but better to fix it.

**Recommended Mitigation:** Round up instead.

**StatusL2:** Fixed in [ff85b3a](https://github.com/status-im/status-network-monorepo/commit/ff85b3a7f1eaba433ba3dc1f5ec1a08158462be9).

**Cyfrin:** Verified.
