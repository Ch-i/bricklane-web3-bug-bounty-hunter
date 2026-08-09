---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Use named mapping parameters to explicitly denote the purpose of keys and values
vuln_class: []
---

# Use named mapping parameters to explicitly denote the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Use named mapping parameters to explicitly denote the purpose of keys and values:
```solidity
off-ramp/BaseOffRamp.sol
43:    mapping(string => bool) public restrictedCountries;

off-ramp/CountryValidator.sol
26:        mapping(string => bool) storage _restrictedCountries

on-ramp/SecuritizeOnRamp.sol
41:    mapping(string => uint256) internal noncePerInvestor;
```

**Securitize:** Fixed in commit [ef5367e](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/ef5367e1db99cb7c72239f5702c817390d23236c).

**Cyfrin:** Verified.
