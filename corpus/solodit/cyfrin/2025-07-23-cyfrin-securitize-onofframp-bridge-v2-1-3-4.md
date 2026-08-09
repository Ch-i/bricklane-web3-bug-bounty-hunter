---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Check for coutry code is not sufficient
vuln_class: []
---

# Check for coutry code is not sufficient

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** In the `CountryValidator` class, the method `validateCountryCode` is intended to check the validity of a given country code. However, it currently does not correctly filter out invalid codes. As a result, inputs such as XX or YYX, which are not valid [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1) (and alpha-2 or alpha-3) country codes, are incorrectly considered valid.

**Recommended Mitigation:** Consider using a map of allowed country codes.

**Securitize:** Acknowledged. Strict ISO country code validation isn't necessary on-chain, as invalid codes are edge cases and can be handled off-chain during onboarding or KYC. On-chain format checks are sufficient for our use case.

**Cyfrin:** Acknowledged.
