---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: Missing zero length check in `AllowedMethodsEnforcer::getTermsInfo()`
vuln_class: []
---

# Missing zero length check in `AllowedMethodsEnforcer::getTermsInfo()`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** The `AllowedMethodsEnforcer` contract's `getTermsInfo()` function correctly validates that the provided terms length is divisible by 4 (as each method selector is 4 bytes), but it fails to reject empty terms (length == 0). Empty terms would technically pass the modulo check since `0 % 4 == 0`, but would result in an empty array of allowed methods.

**Impact:** A delegation with empty terms would never allow any method to be called, as the enforcer would iterate through an empty array of allowed methods and then revert with "AllowedMethodsEnforcer:method-not-allowed" instead of properly rejecting the invalid terms with "AllowedMethodsEnforcer:invalid-terms-length"

**Recommended Mitigation:** Consider adding a specific check to ensure the terms length is greater than zero.

**Metamask:** Fixed in commit [cb2d4d7](https://github.com/MetaMask/delegation-framework/commit/cb2d4d77a66643e541141b3c8291df52340d60ce).

**Cyfrin:** Resolved.
