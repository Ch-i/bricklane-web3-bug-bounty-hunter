---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Emit event in `TokenBridge::removeReserved` when updating storage
vuln_class: []
---

# Emit event in `TokenBridge::removeReserved` when updating storage

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** `TokenBridge::setReserved` emits an event so the opposite function `removeReserved` should likely also emit an event when updating storage.

**Linea:**
Fixed in commit [796f2d9](https://github.com/Consensys/zkevm-monorepo/commit/796f2d9bbacf8c2403b8a4473f9c711172067940#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4R366) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4R370).

**Cyfrin:** Verified.
