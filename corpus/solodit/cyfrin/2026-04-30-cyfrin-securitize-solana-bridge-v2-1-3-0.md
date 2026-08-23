---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: No ownership transfer mechanism for bridge config in either program
vuln_class: []
---

# No ownership transfer mechanism for bridge config in either program

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** Neither program provides an instruction to transfer ownership of the bridge config. The `owner` field is set during `initialize` and all admin operations gate on `has_one = owner`. If the owner key is lost, compromised, or needs rotation (e.g., migrating to a multisig), there is no on-chain mechanism. All admin functions become permanently locked.

**Impact:** Permanent loss of admin control over the bridge. Cannot pause during emergencies, update emitter/bridge addresses, or manage configuration. The program is upgradeable, providing a recovery path, but this depends on the upgrade authority being a different and available key.

**Recommended Mitigation:** Add a two-step ownership transfer pattern:

```rust
// New field in BridgeConfig/UsdcBridgeConfig:
pub pending_owner: Pubkey,

// New instructions:
// propose_owner (owner-only): sets pending_owner
// accept_ownership (pending_owner-only): sets owner = pending_owner, clears pending_owner
```

**Securitize:** Fixed in [983285c](https://github.com/securitize-io/bc-solana-bridge-sc/commit/983285c3a74502c8f74bb9b1fccd2caf17737c26).

**Cyfrin:** Verified.
