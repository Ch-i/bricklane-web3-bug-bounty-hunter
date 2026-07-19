---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: LayerZero integration can be paused but CCIP integration can't be paused
vuln_class: []
---

# LayerZero integration can be paused but CCIP integration can't be paused

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** `MTokenMessagerLZ` has a `bool lzPaused` storage slot and uses `onlyLZNotPaused` modifier to make LayerZero send/receive revert when paused.

In contrast `MTokenMessager` and `MTokenMessagerV2` have no similar pausing functionality for CCIP send/receive.

Consider whether this asymmetry is intentional or whether the CCIP send/receive should similarly be able to be paused.

**Matrixdock:** Acknowledged.
