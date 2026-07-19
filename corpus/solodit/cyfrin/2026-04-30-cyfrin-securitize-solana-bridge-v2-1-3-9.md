---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-9
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
title: '`set_cctp_domain` uses bump value of 0 as sentinel for new account detection'
vuln_class: []
---

# `set_cctp_domain` uses bump value of 0 as sentinel for new account detection

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `SetCctpDomain::handler` checks `cctp_domain.bump == 0` to detect whether the PDA account is newly created vs pre-existing:

```rust
// programs/securitize_usdc_bridge/src/instructions/admin/set_cctp_domain.rs:35-38
require!(
    cctp_domain.bump == 0 || cctp_domain.chain != chain || cctp_domain.domain != domain,
    UsdcBridgeError::CctpDomainUnchanged,
);
```

While unlikely, a valid PDA bump can legitimately be 0, which would cause the "unchanged" check to be bypassed for a pre-existing account with bump=0.

**Recommended Mitigation:** Use an `initialized: bool` field in the `CctpDomain` account, or check if all fields are at their default values instead of relying solely on the bump.

**Securitize:** Fixed in [26f12e5](https://github.com/securitize-io/bc-solana-bridge-sc/commit/26f12e5d32aa327c0dae87c6938ec28db0d36bcf).

Removed the cctp_domain.bump == 0 sentinel and added a require!(chain > 0, InvalidCctpDomainChain) guard at the start of set_cctp_domain - since Wormhole chain ID 0 is unassigned, the default chain == 0 on a freshly init_if_needed-created PDA now serves as an unambiguous uninitialized marker (same pattern used by set_emitter_address in the DS bridge), with no reliance on probabilistic bump-value assumptions.

**Cyfrin:** Confirmed.
