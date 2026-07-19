---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
SecuritizeAmmNavProvider.sol
380:        bool shouldReset = false;

off-ramp/BaseOffRamp.sol
124:        for (uint256 i = 0; i < _countries.length; i++) {
```

**Securitize:** Fixed in commits [7594671](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/75946718b5129603545c364a2d9c6f57902200d9), [6833173](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/68331735079e5964e636c6f139e44649c7903483).

**Cyfrin:** Verified.
