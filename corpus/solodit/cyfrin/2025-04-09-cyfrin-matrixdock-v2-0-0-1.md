---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Users can use transfer and bridging to evade having their tokens frozen via
  the blocklist
vuln_class: []
---

# Users can use transfer and bridging to evade having their tokens frozen via the blocklist

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** One unconventional application of regular transfers or cross-chain transfers via CCIP / LayerZero bridging is to evade the blocklist:
* user sees operator call to `MToken::addToBlockedList` in mempool which would block their address
* user front-runs this transaction by a normal transfer or a CCIP / LayerZero cross-chain transfer to bridge their tokens to a new `receiver` address on another chain
* if the operator attempts to call `MToken::addToBlockedList` on the other chain for the new `receiver` address, the user can bridge back to another new address again

To prevent this the operator can:
* pause bridging (pausing has been implemented for LayerZero but not CCIP) prior to calling `MToken::addToBlockedList`
* use a service such as [flashbots](https://www.flashbots.net/) when calling `MToken::addToBlockedList` so the transaction is not exposed in a public mempool

**Matrixdock:** Acknowledged.
