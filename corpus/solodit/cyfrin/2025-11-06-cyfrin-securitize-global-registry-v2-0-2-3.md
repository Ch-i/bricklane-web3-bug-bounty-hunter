---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Use event indexing for faster off-chain parameter lookup
vuln_class: []
---

# Use event indexing for faster off-chain parameter lookup

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** Events in `IGlobalRegistryService` should use `indexed` keywords on the 3 most important parameters per event to enable faster lookup by those parameters off-chain.

**Securitize:** Fixed in commit [0c2321a](https://github.com/securitize-io/bc-global-registry-service-sc/commit/0c2321ab92e5bd47a602d55e765f18d8b7e7fbdf).

**Cyfrin:** Verified.
