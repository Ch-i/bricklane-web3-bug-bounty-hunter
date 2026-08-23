---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-17
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`ComplianceServiceRegulated::getServices` should use constants from `ComplianceServiceLibrary`
  when setting array indexes'
vuln_class: []
---

# `ComplianceServiceRegulated::getServices` should use constants from `ComplianceServiceLibrary` when setting array indexes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceServiceRegulated::getServices` should use constants from `ComplianceServiceLibrary` when setting array indexes:
```solidity
function getServices() internal view returns (address[] memory services) {
    services = new address[](6);
    services[ComplianceServiceLibrary.DS_TOKEN] = getDSService(DS_TOKEN);
    services[ComplianceServiceLibrary.REGISTRY_SERVICE] = getDSService(REGISTRY_SERVICE);
    services[ComplianceServiceLibrary.WALLET_MANAGER] = getDSService(WALLET_MANAGER);
    services[ComplianceServiceLibrary.COMPLIANCE_CONFIGURATION_SERVICE] = getDSService(COMPLIANCE_CONFIGURATION_SERVICE);
    services[ComplianceServiceLibrary.LOCK_MANAGER] = getDSService(LOCK_MANAGER);
    services[ComplianceServiceLibrary.COMPLIANCE_SERVICE] = address(this);
}
```

**Securitize:** Acknowledged.
