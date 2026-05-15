---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Consider limiting max royalty to prevent large amount or all of the sale fee
  being taken as royalty
vuln_class: []
---

# Consider limiting max royalty to prevent large amount or all of the sale fee being taken as royalty

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** Currently `updateRoyalties` and `setTokenRoyalty` allow the contract owner to set a royalty up to `10_000` which would take the entire sale fee as a royalty. Consider limiting these functions to set the max royalty to something more reasonable like 1000 (10%).

**CryptoArt:**
Fixed in commit [1d1125e](https://github.com/cryptoartcom/cryptoart-smart-contracts/commit/1d1125e5a021f2926dc2a2e39e05c065e3bd207c).

**Cyfrin:** Verified.
