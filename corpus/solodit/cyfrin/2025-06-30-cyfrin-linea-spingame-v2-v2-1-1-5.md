---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: '`latestPrizeId` name is misleading'
vuln_class: []
---

# `latestPrizeId` name is misleading

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** As part of changes in this audit, the `latestPrizeId` variable now functions as a counter for the next available prize ID, rather than tracking the most recently used one as in the previous version. This creates a naming mismatch, since `latestPrizeId` no longer reflects its actual behavior.

The function `_addPrizes` even caches it as `nextPrizeId`, which is a more accurate description. Consider renaming it as `nextPrizeId`.

**Linea:** Fixed in commits [`8266a91`](https://github.com/Consensys/linea-hub/pull/555/commits/8266a9130db2e3ad9d66422c7c1c374dc806bada) and [`dd8de7b`](https://github.com/Consensys/linea-hub/pull/555/commits/dd8de7bd9626abca6c01bc24832551c8f50ef0a9)

**Cyfrin:** Verified. Field renamed to `nextPrizeId` and stack variable in `__addPrizes` renamed to `currentPrizeId`.

\clearpage
