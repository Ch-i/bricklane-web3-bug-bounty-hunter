---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-16
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Cache compliance service and compliance configuration service for much cleaner
  code in `ComplianceServiceRegulated::completeTransferCheck`
vuln_class: []
---

# Cache compliance service and compliance configuration service for much cleaner code in `ComplianceServiceRegulated::completeTransferCheck`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceServiceRegulated::completeTransferCheck` has a lot of `if` statements which are very large and hard to understand as they are full of `ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE])` and `IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE])`.

This can be easily improved by caching those two values into local variables:
```solidity
ComplianceServiceRegulated complServiceReg = ComplianceServiceRegulated(_services[COMPLIANCE_SERVICE]);
IDSComplianceConfigurationService complConfigService
    = IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]);
```

Then in the `if` conditions just use `complServiceReg` and `complConfigService` which massively simplifies them vastly improving readability.

**Securitize:** Acknowledged; this was analyzed in the past and there is an intentional balance when using local variables. Historically, we've had many issues with errors like "Stack Too Deep" when using too many of them, and they did not improve readability or gas usage too much. We prefer to not go through this process again because it's currently working as intended.
