---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Emit missing events on important parameter changes
vuln_class: []
---

# Emit missing events on important parameter changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Emit missing events on important parameter changes:
* `CCTPSender::setCCTPDomain`
* `USDCBridgeV2::setCCTPDomain`

**Securitize:** Fixed in commit [cd8c8ad](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/cd8c8ada1240c862458138cc1db9372aaf970573) for `USDCBridgeV2`, leaving the other as it will be deprecated.

**Cyfrin:** Verified.
