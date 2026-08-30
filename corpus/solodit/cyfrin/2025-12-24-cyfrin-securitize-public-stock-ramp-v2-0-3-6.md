---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Use named return variables where this can refactor away local variables
vuln_class: []
---

# Use named return variables where this can refactor away local variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Use named return variables where this can refactor away local variables:
* `CountryValidator::getCountry`
* `PublicStockOnRamp::calculateDsTokenAmount` - read result of `navProvider.quoteBuyBase` directly into `rate` and remove local variable `execPrice`

**Securitize:** Fixed in commit [f6055a0](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/f6055a0a59d63360a6bd8c6aee6c8ca3631832e7).

**Cyfrin:** Verified.
