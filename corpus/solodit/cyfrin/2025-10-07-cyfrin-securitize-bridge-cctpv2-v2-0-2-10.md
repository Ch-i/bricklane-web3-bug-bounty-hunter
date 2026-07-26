---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Uninitialized country for valid investor wallets allows bypassing US compliance
  lockup period
vuln_class: []
---

# Uninitialized country for valid investor wallets allows bypassing US compliance lockup period

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** One way that wallets can be registered in the protocol is via `RegistryService.sol::addWallet`, meanwhile the country field for the registered wallet can be set separately using a separate function `setCountry`.

Hence there can be a small window during these two transactions which leaves the country field as an empty string (default value) for a valid wallet .

**Impact:** Since during bridging of DS tokens the `country` would be an empty string, the `region` memory variable will also default to 0. This would mean the `lockPeriod` would store and use the non-US lock period:
```solidity
string memory country = registryService.getCountry(investorId);
uint256 region = complianceConfigurationService.getCountryCompliance(country);

uint256 lockPeriod = (region == US) ? complianceConfigurationService.getUSLockPeriod() : complianceConfigurationService.getNonUSLockPeriod();
        uint256 availableBalanceForTransfer = complianceService.getComplianceTransferableTokens(_msgSender(), block.timestamp, uint64(lockPeriod));
```

This is problematic since:
1. Uninitialized country fields for valid wallets are allowed to perform bridging
2. If the intended country = US, the lockPeriod uses the non-US lock period instead.

This small period of time can be used by malicious wallet owners to use a lower `lockPeriod` (if non-US lock time is smaller than US lock time).

**Recommended Mitigation:** Check if country is an empty string in `validateLockedTokens` and revert if true.

**Securitize:** Acknowledged; If the investor is bridging tokens, they were already minted/issued. Hence compliance rules were validated including country and region at the time of token minting/issuance.
