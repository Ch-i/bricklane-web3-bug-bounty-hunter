---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-15-cyfrin-story-ip-derivative-agent-v2-1-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md
tags:
- firm:cyfrin
- report:2026-01-15-cyfrin-story-ip-derivative-agent-v2-1
title: '`CommercializerChecker` Access Control Bypass via `IPDerivativeAgent`'
vuln_class: []
---

# `CommercializerChecker` Access Control Bypass via `IPDerivativeAgent`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md)_

---

**Description:** When `IPDerivativeAgent::registerDerivativeViaAgent` is used, the agent contract acts as an intermediary and calls `LicensingModule::registerDerivative` on behalf of the user. As a result, the agent contract address is propagated as the caller / licensee throughout the verification flow.

In LicensingModule:
```solidity
   if (
       !ILicenseTemplate(licenseTemplate).verifyRegisterDerivativeForAllParents(
           childIpId,
           parentIpIds,
           licenseTermsIds,
           msg.sender  // This is the agent contract address
       )
   ) {
       revert Errors.LicensingModule__LicenseNotCompatibleForDerivative(childIpId);
   }
```

In `LicensingModule::verifyRegisterDerivativeForAllParents`, the caller parameter is derived from `msg.sender`, which in this case is the agent contract. This value is then forwarded to the `commercializerChecker` hook and used as the licensee parameter during verification.

```solidity
  // Check if the commercializerChecker allows the link
   if (terms.commercializerChecker != address(0)) {
       if (
           !IHookModule(terms.commercializerChecker).verify(
               parentIpId,
               licensee,  // This is the agent address, not the actual user
               terms.commercializerCheckerData
           )
       ) {
           return false;
       }
   }
```


Consequently, `commercializerChecker` implementations observe and validate the agent address rather than the actual end user initiating the request. Hook logic that assumes the licensee corresponds to the end user (e.g., blacklists, allowlists, or compliance checks) may therefore behave differently when invoked via the agent.

It is unclear whether this behavior is an intentional design decision or an implicit consequence of the agent abstraction.


**Impact:** This behavior does not represent a direct vulnerability and may be intended. The practical impact is limited to a semantic difference between agent-based and direct interactions with LicensingModule.

In the worst case, a restricted end user could register a derivative through the agent for a parent–child IP combination that is otherwise globally allowed. This does not bypass parent-level authorization, but may differ from expectations of hook implementations that assume end-user–level enforcement.

**Recommended Mitigation:** The relevant behavior could be explicitly documented, such as " the agent overrides the hook".

**Story:** Acknowledged.

\clearpage
