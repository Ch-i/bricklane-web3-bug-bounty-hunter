---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-L-1 LSP0 ownership functions deviate from specification and reject native
  tokens
vuln_class: []
---

# TRST-L-1 LSP0 ownership functions deviate from specification and reject native tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
The LSP specifications define the following functions for LSP0:
```solidity
    function transferOwnership(address newPendingOwner) external payable;
    function renounceOwnership() external payable;
```
However, their implementations are not payable.
```solidity
    function transferOwnership(address newOwner) public virtual
        override(LSP14Ownable2Step, OwnableUnset)
    {
```
```solidity
    function renounceOwnership() public virtual override(LSP14Ownable2Step, OwnableUnset) {
         address _owner = owner();
```
This may break interoperation between conforming and non-confirming contracts.

**Recommended Mitigation:**
Remove the payable keyword in the specification for the above functions, or make the 
implementations payable

**Team Response:**
Team response
Fixed in Specs
