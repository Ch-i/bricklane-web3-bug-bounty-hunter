---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-14
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Perform local variable checks first prior to external calls in composite `if`
  statement conditions
vuln_class: []
---

# Perform local variable checks first prior to external calls in composite `if` statement conditions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** When an `if` statement condition is joined together using `&&` operators from multiple composite parts, local variable checks should be performed first prior to external calls. This is because if the local variable checks evaluate to `false` there is no need to then perform the external calls.

Three places where this occurs is in `ComplianceServiceRegulated::completeTransferCheck`:
```solidity
253:            if (IDSComplianceConfigurationService(
254:                   _services[COMPLIANCE_CONFIGURATION_SERVICE]).getForceFullTransfer() &&
255:                _args.fromInvestorBalance > _args.value
256:            ) {

272:            if (IDSComplianceConfigurationService(.
273:                   _services[COMPLIANCE_CONFIGURATION_SERVICE]).getWorldWideForceFullTransfer() &&
274:                _args.fromInvestorBalance > _args.value
275:            ) {
```

Instead perform the local variable checks first:
```solidity
            if (_args.fromInvestorBalance > _args.value &&
                IDSComplianceConfigurationService(
                   _services[COMPLIANCE_CONFIGURATION_SERVICE]).getForceFullTransfer()
            ) {

            if (_args.fromInvestorBalance > _args.value &&
                IDSComplianceConfigurationService(
                   _services[COMPLIANCE_CONFIGURATION_SERVICE]).getWorldWideForceFullTransfer()
            ) {
```

Similar optimization can be applied to:
* L284->287 EU check
* L290->292 accreditation check

**Securitize:** **Cyfrin:**
