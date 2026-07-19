---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Stale `ResolverConfig` PDA persists when emitter address is updated in-place
vuln_class: []
---

# Stale `ResolverConfig` PDA persists when emitter address is updated in-place

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `SetEmitterAddress::handler` uses `init_if_needed` for the `EmitterAddress` PDA (same seeds since chain unchanged) but creates a new `ResolverConfig` PDA (new seeds since address changed via `init`). The old `ResolverConfig` (seeded by the old address) is not closed, becoming orphaned.

**Impact:** Orphaned PDAs waste ~0.002 SOL rent each. No functional impact -- the resolver correctly derives from the active emitter address.

**Recommended Mitigation:** Accept the old `ResolverConfig` as an optional account in `set_emitter_address` and close it when the address changes. Alternatively, seed `ResolverConfig` by chain only (not address).

**Securitize:** Fixed in [923f917](https://github.com/securitize-io/bc-solana-bridge-sc/commit/923f917e0cd8a29bbfbba99da21458549d8f9d82).

**Cyfrin:** Verified.
