---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Refactor `SecuritizeBridge::validateLockedTokens` to take `dsServiceConsumer`
  as input parameter
vuln_class: []
---

# Refactor `SecuritizeBridge::validateLockedTokens` to take `dsServiceConsumer` as input parameter

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `SecuritizeBridge::bridgeDSTokens` at L77 reads `dsServiceConsumer` from storage then at L83 calls `validateLockedTokens`.

The internal function `validateLockedTokens` itself re-reads `dsServiceConsumer` from storage multiple times.

Reading from storage is expensive; instead:
* cache `dsServiceConsumer` once in `bridgeDSTokens`
* refactor `validateLockedTokens` to take `dsServiceConsumer` as an input parameter
* in `bridgeDSTokens` when calling `validateLockedTokens` pass the cached `dsServiceConsumer` as an input parameter

**Securitize:** Fixed in commits [bcc83e0](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/bcc83e04b66320b07fcc621352de72e59985bf8a), [0cf5dd9](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/0cf5dd91a4ff6ba1d2a1d5c9b55c395e415536e1).

**Cyfrin:** Verified.
