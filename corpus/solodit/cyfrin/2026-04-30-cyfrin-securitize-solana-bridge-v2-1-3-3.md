---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Dead Code Where `country_string_to_u8` and `CctpDomainNotConfigured` Are Not
  Used
vuln_class: []
---

# Dead Code Where `country_string_to_u8` and `CctpDomainNotConfigured` Are Not Used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

Finding:

**Description:** Two pieces of dead code exist across the bridge programs:

1. `country_string_to_u8` in `programs/securitize_bridge/src/utils/country.rs:6` — a ~200-line function mapping ISO alpha-2 codes and country names to `u8` values with zero callers in the codebase.

2. `UsdcBridgeError::CctpDomainNotConfigured` — an error variant declared in the USDC bridge error enum with no references anywhere in the program.

**Recommended Mitigation:** Remove `utils/country.rs` and its module declaration in `utils/mod.rs`. Remove the `CctpDomainNotConfigured` variant from `UsdcBridgeError`.

**Securitize:** Fixed in [1626344](https://github.com/securitize-io/bc-solana-bridge-sc/commit/162634433e9301fa0ac91d79e7c8c1a1be8c49dd).

Removed country_string_to_u8 (along with utils/country.rs and its module declaration) and the unused UsdcBridgeError::CctpDomainNotConfigured variant.

**Cyfrin:** Confirmed.
