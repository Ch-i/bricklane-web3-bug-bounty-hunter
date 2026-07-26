---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-1-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-M-6 KeyManager ERC165 does not support LSP20
vuln_class: []
---

# TRST-M-6 KeyManager ERC165 does not support LSP20

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:** 
LSP6KeyManager supports LSP20 call verification. However, in `supportInterface()` it does not 
return the LSP20 **interfaceId**.
```solidity
    function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) {
    return
    interfaceId == _INTERFACEID_LSP6 || interfaceId == _INTERFACEID_ERC1271 ||
        super.supportsInterface(interfaceId);
           }
```
As a result, clients which correctly check for support of LSP20 methods will not operate with 
the KeyManager implementation.

**Recommended Mitigation:**
Insert another supported **interfaceId** under `supportsInterface()`.

**Team response:**
Fixed (applied recommendation) 

**Mitigation review:**
Fixed. An additional non-conforming ERC165 interface was created for verification clients, is 
a design decision.
