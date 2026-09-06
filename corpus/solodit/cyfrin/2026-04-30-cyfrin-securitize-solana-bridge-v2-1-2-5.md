---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Country source inconsistency between lock validation and cross-chain payload
  in `bridge_ds_tokens`
vuln_class: []
---

# Country source inconsistency between lock validation and cross-chain payload in `bridge_ds_tokens`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** In `BridgeDsTokens::handler`, `identity.country` (from `IdentityAccount`) is used for lock validation (line 303 via `validate_locked_tokens`), while `ctx.accounts.investor.country` (from `ImrInvestor`) is used for the cross-chain payload (line 331). These come from different external programs (`identity_registry` and `rwa_imr` respectively) and could theoretically diverge.

**Impact:** If country values diverge, the wrong lock period may be applied (US vs non-US), or the cross-chain payload may carry an incorrect country. Both sources are from the Securitize identity system and expected to be synchronized.

**Recommended Mitigation:** Add an explicit check:

```rust
require!(
    identity.country == ctx.accounts.investor.country,
    BridgeError::CountryMismatch,
);
```

**Securitize:** Fixed in [9fc5b8fc](https://github.com/securitize-io/bc-solana-bridge-sc/commit/9fc5b8fc55b409ce40f86a848a504a26c39282f7).

Resolved by making IdentityAccount the single source of truth for country: the outbound payload now reads identity.country instead of investor.country, matching the account already used for locked-tokens validation (and mirroring the EVM flow where both checks read from the same IDSRegistryService). This eliminates divergence structurally, so the explicit require!(identity.country == investor.country) check is no longer needed.

**Cyfrin:** Confirmed.
