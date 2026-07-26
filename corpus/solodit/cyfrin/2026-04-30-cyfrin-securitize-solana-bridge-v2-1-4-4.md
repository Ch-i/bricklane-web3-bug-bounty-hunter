---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-4-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Redundant immutable borrow in `set_bridge_address` and `set_emitter_address`
vuln_class: []
---

# Redundant immutable borrow in `set_bridge_address` and `set_emitter_address`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** In both `SetBridgeAddress::handler` and `SetEmitterAddress::handler`, an immutable reference is taken for a check, then immediately replaced by a mutable reference to the same account:

```rust
// programs/securitize_bridge/src/instructions/admin/set_bridge_address.rs:46-53
let existing = &ctx.accounts.bridge_address;
require!(
    existing.chain != chain || existing.address != address,
    BridgeError::BridgeAddressUnchanged,
);
let bridge_address = &mut ctx.accounts.bridge_address;
```

Same pattern in `set_emitter_address.rs:59-66`.

**Recommended Mitigation:** Take the mutable reference once and use it for both the check and mutation.

**Securitize:** Fixed in [c51e5e57b](https://github.com/securitize-io/bc-solana-bridge-sc/commit/c51e5e57bb49c185ac5efe7da10a20eb799f823d).

Taking a single mutable borrow and reusing it for both the unchanged-value check and the mutation in set_bridge_address::handler and set_emitter_address::handler.

**Cyfrin:** Confirmed.


\clearpage
