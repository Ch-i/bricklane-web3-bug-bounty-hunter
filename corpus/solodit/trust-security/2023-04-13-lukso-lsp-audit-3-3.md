---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: Better verification
vuln_class: []
---

# Better verification

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

1. In LSP0ERC725AccountCore's `universalReceiver()`, the delegate value can be over 20 
bytes.
```solidity
    bytes memory lsp1DelegateValue = 
       _getData(_LSP1_UNIVERSAL_RECEIVER_DELEGATE_KEY);
           bytes memory resultDefaultDelegate;
              if (lsp1DelegateValue.length >= 20) {
```
It would be better to avoid errors and only call the delegate if length is precisely 20 
bytes.
2. In LSP6ExecuteModule's `_verifyCanExecute()`, the 12 upper bytes of the address 
**uint256** are never parsed.
```solidity
      // MUST be one of the ERC725X operation types.
             uint256 operationType = uint256(bytes32(payload[4:36]));
                address to = address(bytes20(payload[48:68]));
```
Good practice would be to verify they are all zeros. Such issues have the potential to 
lead to high-impact bugs as some address verifications could be bypassed.

**Team response:**
Point #1 acknowledged as a design decision. Point #2 has been fixed.
