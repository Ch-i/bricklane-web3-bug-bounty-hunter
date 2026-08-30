---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-15
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Fast fail without performing unnecessary storage reads or external calls
vuln_class: []
---

# Fast fail without performing unnecessary storage reads or external calls

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Fast fail without performing unnecessary storage reads or external calls. For example in `ComplianceServiceRegulated::preIssuanceCheck` the start of the function looks like this:
```solidity
function preIssuanceCheck(
    address[] calldata _services,
    address _to,
    uint256 _value
) public view returns (uint256 code, string memory reason) {
    ComplianceServiceRegulated complianceService = ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]);
    IDSComplianceConfigurationService complianceConfigurationService = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]);
    IDSWalletManager walletManager = IDSWalletManager(_services[WALLET_MANAGER]);
    string memory toCountry = IDSRegistryService(_services[REGISTRY_SERVICE]).getCountry(IDSRegistryService(_services[REGISTRY_SERVICE]).getInvestor(_to));
    uint256 toRegion = complianceConfigurationService.getCountryCompliance(toCountry);

    if (toRegion == FORBIDDEN) {
        return (26, DESTINATION_RESTRICTED);
    }

    if (!complianceService.checkWhitelisted(_to)) {
        return (20, WALLET_NOT_IN_REGISTRY_SERVICE);
    }
```

But if the function is going to return because `_to` is not whitelisted, then it makes no sense to spend gas performing all the interim unrelated storage reads and external calls. Instead storage reads and external calls should only be made as they are needed, eg:
```solidity
function preIssuanceCheck(
    address[] calldata _services,
    address _to,
    uint256 _value
) public view returns (uint256 code, string memory reason) {
    ComplianceServiceRegulated complianceService = ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]);
    // fail fast if not whitelisted
    if (!complianceService.checkWhitelisted(_to)) {
        return (20, WALLET_NOT_IN_REGISTRY_SERVICE);
    }

    IDSComplianceConfigurationService complianceConfigurationService = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]);

     // don't need this until much later in the function so no point doing it here
    // IDSWalletManager walletManager = IDSWalletManager(_services[WALLET_MANAGER]);

    // add this to improve readability as this is used multiple times
    IDSRegistryService regService = IDSRegistryService(_services[REGISTRY_SERVICE]);

    string memory toCountry = regService.getCountry(regService.getInvestor(_to));
    uint256 toRegion = complianceConfigurationService.getCountryCompliance(toCountry);

    if (toRegion == FORBIDDEN) {
        return (26, DESTINATION_RESTRICTED);
    }

    // continue remaining processing, following the principles of failing fast by only
    // perform storage reads and external calls as they are needed
```

**Securitize:** Fixed in commit [80d536e](https://github.com/securitize-io/dstoken/commit/80d536ec48d316b08226fbe53ee8a0e793ec074a).

**Cyfrin:** Verified.
