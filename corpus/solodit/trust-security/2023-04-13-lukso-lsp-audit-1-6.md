---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-1-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-M-7 Incorrect permission check due to confusion between empty call and
  the zero selector
vuln_class: []
---

# TRST-M-7 Incorrect permission check due to confusion between empty call and the zero selector

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
In case the caller of LSP6 does not have **_PERMISSION_SUPER_CALL**, `_verifyAllowedCall()` is 
called to check they have specific permissions for the call. It will use the function 
`_extractExecuteParameters()` to get the call selector.
```solidity
    // CHECK if there is at least a 4 bytes function selector
    bytes4 selector = executeCalldata.length >= 168
       ? bytes4(executeCalldata[164:168]) : bytes4(0);
           return (operationType, to, value, selector);
```
Due to the behavior above, the 0x00000000 selector would be confused with an empty call. 
Later in `_extractCallType()`, the call will not be marked as requiring **_ALLOWEDCALLS_WRITE** 
permission, if it's passing value.
```solidity
      if (operationType == OPERATION_0_CALL) {
      if (
      // CHECK if we are doing an empty call
          (selector == bytes4(0) && value == 0) ||
      // we do not require callType CALL
      // if we are just transferring value without `data`
          selector != bytes4(0)
       ) {
           requiredCallTypes = _ALLOWEDCALLS_WRITE;
           }
      }
```
As a result, a user that has transfer permission but not write permission for 0xFFFFFFFF 
(function wildcard), will be permitted to pass calldata to the fallback function. The fallback as 
implemented in LSP0ERC725AccountCore would look up the extension for 0x00000000 
selector and call it.

**Recommended mitigation:**
Consider adding an **isEmptyCall** parameter to `_extractCallType()`. If it is not true, 
**_ALLOWEDCALLS_WRITE** should be turned on even for selector 0x00000000.

**Team response:**
Fixed (applied recommendation).

**Mitigation review:**
Fixed
