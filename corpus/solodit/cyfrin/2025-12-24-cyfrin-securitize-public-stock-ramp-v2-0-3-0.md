---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Better storage packing by changing declaration order
vuln_class: []
---

# Better storage packing by changing declaration order

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Better storage packing by changing declaration order:
* `2-nav-provider/contracts/nav/SecuritizeAmmNavProvider.sol` - declare `lastMarketStatus` immediately after `asset`:
```solidity
IERC20Metadata public asset;
uint8 public lastMarketStatus;
```

**Securitize:** Fixed in commit [41815fa](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/41815fa7c45fe54ed46ed3d87aa81ea1a57af3fb).

**Cyfrin:** Verified.
