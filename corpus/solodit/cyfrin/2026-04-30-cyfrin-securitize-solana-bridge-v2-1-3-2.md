---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`ResolverConfig` PDA uses big-endian chain seed while other chain-seeded PDAs
  use little-endian'
vuln_class: []
---

# `ResolverConfig` PDA uses big-endian chain seed while other chain-seeded PDAs use little-endian

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `EmitterAddress` and `BridgeAddress` PDAs use `chain.to_le_bytes()` for the chain seed. `ResolverConfig` uses `chain.to_be_bytes()`. All usages within each PDA type are internally consistent, so there is no current functional bug. The inconsistency within a single instruction file (`set_emitter_address.rs` uses LE on line 28 and BE on line 40) is a maintainability hazard.

**Impact:** No current vulnerability. Risk of introducing bugs in future code changes if a developer copies the LE pattern from the adjacent `EmitterAddress` derivation for a `ResolverConfig` lookup.

**Recommended Mitigation:** Standardize on `to_le_bytes()` for `ResolverConfig` to match all other chain-seeded PDAs. Update `set_emitter_address.rs:40`, `remove_emitter_address.rs:38`, and `resolver.rs:54`.

**Securitize:** Fixed in [d1e8acb](https://github.com/securitize-io/bc-solana-bridge-sc/commit/d1e8acbf6dac80803a7948e8e7c4ed730a373378).

Adopted the recommendation. ResolverConfig PDA derivation now uses chain.to_le_bytes() at all four sites.

**Cyfrin:** Confirmed.
