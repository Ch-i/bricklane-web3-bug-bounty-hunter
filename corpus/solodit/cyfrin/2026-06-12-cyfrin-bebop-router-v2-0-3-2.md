---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopPmmHelper::_decodeSinglePmm, _decodeAggregatePmm` read `eventId` from
  unsigned PMM flags, letting a taker spoof emitted event identifiers'
vuln_class: []
---

# `BebopPmmHelper::_decodeSinglePmm, _decodeAggregatePmm` read `eventId` from unsigned PMM flags, letting a taker spoof emitted event identifiers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `pmm.eventId` is extracted as `uint128(pmmFlags >> 128)` from the PMM order's `flags` word (`contracts/base/BebopPmmHelper.sol:89` for single orders, `:135` for aggregate orders). In the out-of-scope `BebopSettlement`, the `flags` field is explicitly excluded from the maker signature hash - it is not a signed field. The router also does not sign or validate `eventId`. Because `bebopPmmCalldata` is caller-supplied, any taker can set an arbitrary value in the upper 128 bits of `pmmFlags` without invalidating the maker's signature. Both `BebopPmmSwap` and `BebopRouterSwap` are emitted with this attacker-chosen `eventId` (`contracts/BebopRouter.sol:312-318, 537-547`). Off-chain indexers or accounting systems that key on `eventId` for fill attribution can therefore be fed spoofed or colliding identifiers. On-chain fund flows are unaffected; the impact is confined to observability and off-chain accounting integrity.

**Recommended Mitigation:** If `eventId` must be trustworthy for off-chain consumers, bind it into a signed field - either in the router order (adding it to the `ORDER_TYPE_HASH` fields) or in the maker PMM order. If `eventId` is intentionally untrusted, document this explicitly so off-chain consumers do not rely on it for fill attribution.

**Bebop:** Acknowledged.
