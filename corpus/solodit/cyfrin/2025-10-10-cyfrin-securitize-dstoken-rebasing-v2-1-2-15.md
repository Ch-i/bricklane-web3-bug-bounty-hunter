---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-15
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`ComplianceServiceRegulated::preIssuanceCheck` allows issuance to non-accredited
  investors when `forceAccredited` or `forceAccreditedUS` is set, and allows issuance
  below regional minimum thresholds, violating compliance requirements'
vuln_class: []
---

# `ComplianceServiceRegulated::preIssuanceCheck` allows issuance to non-accredited investors when `forceAccredited` or `forceAccreditedUS` is set, and allows issuance below regional minimum thresholds, violating compliance requirements

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceServiceRegulated::completeTransferCheck` has several checks that `preIssuanceCheck` is missing:

1) Force Accredited

`completeTransferCheck` verifies whether force accredited is enabled and if so only allow transfers to accredited investors:
```solidity
bool isAccreditedTo = isAccredited(_services, _args.to);
if (
    IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getForceAccredited() && !isAccreditedTo
) {
    return (61, ONLY_ACCREDITED);
}

} else if (toRegion == US) {
    if (
        IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getForceAccreditedUS() &&
        !isAccreditedTo
    ) {
        return (62, ONLY_US_ACCREDITED);
    }
```

But `preIssuanceCheck` doesn't enforce this, so it could allow issuance to unaccredited investors even when `ForceAccredited` or `ForceAccreditedUS` is enabled.

2) Regional Minimal Token Holdings

`completeTransferCheck` verifies regional minimum token holdings eg:
```solidity
if (toInvestorBalance + _value < IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getMinUSTokens()) {
    return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
}
```
But preIssuanceCheck only verifies the generic minimum holdings:
```solidity
        if (
            !walletManager.isPlatformWallet(_to) &&
        balanceOfInvestorTo + _value < complianceConfigurationService.getMinimumHoldingsPerInvestor()
        ) {
            return (51, AMOUNT_OF_TOKENS_UNDER_MIN);
        }
```

Hence `preIssuanceCheck` could result in users being issued an amount of tokens that violates their regional minimum token holdings.

**Impact:** `ComplianceServiceRegulated::preIssuanceCheck` allows issuance to non-accredited investors when `forceAccredited` or `forceAccreditedUS` is set, and allows issuance below regional minimum thresholds, violating compliance requirements

**Recommended Mitigation:** Enforce the above checks in `ComplianceServiceRegulated::preIssuanceCheck`.

**Securitize:** Fixed in commits [4991826](https://github.com/securitize-io/dstoken/commit/499182670e4b05c0a8f5eefc639403e5dbaf15bd), [0656ccd](https://github.com/securitize-io/dstoken/commit/0656ccd7e48af296770bcf780a47c3a14fcc9eba).

**Cyfrin:** Verified.
