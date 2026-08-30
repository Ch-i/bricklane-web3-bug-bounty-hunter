---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Rename `SecuritizeBridge::whChainId` to `whRefundChainId`
vuln_class: []
---

# Rename `SecuritizeBridge::whChainId` to `whRefundChainId`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** The only purpose of `SecuritizeBridge::whChainId` is to be the wormhole refund chain id; rename it to something like `whRefundChainId` which accurately describes its purpose.

Also there are no functions to change this value; consider adding one if this may be required.

**Securitize:** Acknowledged.
