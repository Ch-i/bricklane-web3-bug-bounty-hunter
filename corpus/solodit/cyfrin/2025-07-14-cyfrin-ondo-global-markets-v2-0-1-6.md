---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: Confusing field name `minimumLiveness` in `PriceData` struct
vuln_class: []
---

# Confusing field name `minimumLiveness` in `PriceData` struct

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** The [`PriceData`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/sanityCheckOracle/OndoSanityCheckOracle.sol#L37-L49) struct in `OndoSanityCheckOracle` includes a field named `minimumLiveness`, which actually represents the maximum age a price can be before it's considered stale. The current name may be misleading, as "minimum liveness" implies a lower bound on freshness rather than an upper bound on staleness.

Consider renaming the field to something clearer like `maxPriceAge` or `staleThreshold` to better reflect its purpose and improve code readability.

**Ondo:** Fixed in commits [`b453b57`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/b453b57a8785ee7905d8dc46bee47694f43f152c) and [`9af9735`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/9af9735587341a0c97a04ce00ace905406b87e8c)

**Cyfrin:** Verified. Renamed to `maxTimeDelay`.
