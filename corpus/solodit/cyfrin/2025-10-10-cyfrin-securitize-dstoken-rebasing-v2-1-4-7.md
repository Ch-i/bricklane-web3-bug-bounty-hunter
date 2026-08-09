---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Remove setting deprecated `lastUpdatedBy` in RegistryService
vuln_class: []
---

# Remove setting deprecated `lastUpdatedBy` in RegistryService

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The client has informed us that `lastUpdatedBy` is deprecated so it should not be updated in `RegistryService`:
```solidity
registry/RegistryService.sol
113:        investors[_id].lastUpdatedBy = msg.sender;
140:        investors[_id].lastUpdatedBy = msg.sender;
```

Additionally a comment should be placed to indicate this in the relevant data store:
```solidity
data-stores/RegistryServiceDataStore.sol
33:        address lastUpdatedBy;
40:        address lastUpdatedBy;
```

Or the storage slots should be renamed to `DEPRECATED_lastUpdatedBy` as has been done in other places for deprecated storage slots.

**Securitize:** Fixed in commit [9a80a47](https://github.com/securitize-io/dstoken/commit/9a80a478fffcf7ef81e5c0ca229ab2ff4efc7b9e) by no longer writing to `lastUpdatedBy` and in commit [e6165e4](https://github.com/securitize-io/dstoken/commit/e6165e4ae5c29ca1787bbf90dd62c83a6e915ba6) by renaming the variable to explicitly indicate it is deprecated.

**Cyfrin:** Verified.
