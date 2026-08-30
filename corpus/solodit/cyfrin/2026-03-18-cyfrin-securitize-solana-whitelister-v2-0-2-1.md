---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: '`set_require_investor_signature` allows setting to current value, emitting
  misleading event'
vuln_class: []
---

# `set_require_investor_signature` allows setting to current value, emitting misleading event

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** `set_require_investor_signature` unconditionally sets the flag and emits a `RequireInvestorSignatureUpdated` event, even when the new value equals the current value. This produces misleading events suggesting a configuration change occurred when none did.

**Recommended Mitigation:** Add a guard to prevent no-op updates:

```rust
require!(
    state.require_investor_signature != require_investor_signature,
    VaultRegistrarError::AlreadySet // new error code
);
```

**Securitize:** Fixed in [3c93d56](https://github.com/securitize-io/bc-solana-whitelister/commit/3c93d56a0296d9cada6eb556fa8674dff0933689).

**Cyfrin:** Verified.
