---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Redundant Access Control Check in `SecuritizeInternalNavProvider::addRateUpdater,
  removeRateUpdater`
vuln_class: []
---

# Redundant Access Control Check in `SecuritizeInternalNavProvider::addRateUpdater, removeRateUpdater`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeInternalNavProvider::addRateUpdater, removeRateUpdater` perform redundant access control checks. These functions have an `onlyRole(DEFAULT_ADMIN_ROLE)` modifier, but then call `grantRole/revokeRole` which internally perform the same check:

```solidity
  function addRateUpdater(address _account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(RATE_UPDATER, _account);
        emit RateUpdaterAdded(_account);
    }
```
Since `RATE_UPDATER` admin role defaults to `DEFAULT_ADMIN_ROLE`, both checks require the same role, resulting in duplicate authorization verification and unnecessary gas consumption.

**Recommended Mitigation:** Use the internal `_grantRole` and `_revokeRole` functions directly since access control is already enforced by the function modifiers:

**Securitize:** Fixed in commit [77a9a52](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/77a9a5295ca55f3d62df3ecc8517217598bf4deb).

**Cyfrin:** Verified.
