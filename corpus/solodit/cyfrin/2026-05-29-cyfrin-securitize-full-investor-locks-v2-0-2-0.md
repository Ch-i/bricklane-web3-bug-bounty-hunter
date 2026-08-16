---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceLibrary::completeTransferCheck` EU retail cap lacks the
  `!= 0` guard'
vuln_class: []
---

# `ComplianceServiceLibrary::completeTransferCheck` EU retail cap lacks the `!= 0` guard

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceLibrary::completeTransferCheck` at `contracts/compliance/ComplianceServiceRegulated.sol:342-344` enforces the EU retail cap without the `!= 0` guard that all four sibling regional caps in the same function carry (JP at line 332, US at 367, US-accredited at 376, total at 400). The mirror site in `ComplianceServiceLibrary::preIssuanceCheck` at line 513-514 has the same omission.

When `getEURetailInvestorsLimit() == 0` - the natural way to express "no EU retail cap" and the default state of a fresh deployment - the comparison `getEURetailInvestorsCount(country) >= 0` is trivially true. The cap rejects every fresh EU retail transfer and every fresh EU retail issuance with `(40, MAX_INVESTORS_IN_CATEGORY)`.

**Recommended Mitigation:** Add the `!= 0` guard to both call sites, mirroring the sibling caps.

At `contracts/compliance/ComplianceServiceRegulated.sol:342`, prepend `IDSComplianceConfigurationService(_services[COMPLIANCE_CONFIGURATION_SERVICE]).getEURetailInvestorsLimit() != 0 &&` to the cap predicate.

At `contracts/compliance/ComplianceServiceRegulated.sol:513`, prepend `complianceConfigurationService.getEURetailInvestorsLimit() != 0 &&` to the predicate in `preIssuanceCheck`.

**Files:**

- `ComplianceServiceLibrary::completeTransferCheck`
- `ComplianceServiceLibrary::preIssuanceCheck`


**Securitize:** Acknowledged.
