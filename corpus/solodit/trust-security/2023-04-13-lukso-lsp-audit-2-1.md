---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-L-2 Transfers of vaults from an invalid source are not treated correctly
  by receiver delegate
vuln_class: []
---

# TRST-L-2 Transfers of vaults from an invalid source are not treated correctly by receiver delegate

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
In the universalReceiver() function, if the notifying contract does not support LSP9, yet the 
**typeID** corresponds to an LSP9 transfer, the function will return instead of reverting.
```solidity
    if (
      mapPrefix == _LSP10_VAULTS_MAP_KEY_PREFIX && notifier.code.length > 0 &&
         !notifier.supportsERC165InterfaceUnchecked(_INTERFACEID_LSP9)
    ) {
        return "LSP1: not an LSP9Vault ownership transfer";
     }
```

**Recommended Mitigation:**
Revert when dealing with transfers that cannot be valid.

**Team Response:**
Refactored with a different logic.

**Mitigation review:**
The code above has been removed. This validation indeed does not seem to be necessary.
