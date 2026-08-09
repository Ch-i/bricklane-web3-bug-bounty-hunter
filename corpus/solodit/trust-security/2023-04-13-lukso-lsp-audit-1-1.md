---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-1-1
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
title: TRST-M-2 Deviation from spec will result in dislocation of receiver delegate
vuln_class: []
---

# TRST-M-2 Deviation from spec will result in dislocation of receiver delegate

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
The LSP0 `universalReceiver()` function looks up the receiver delegate by crafting a mapping key 
type.
```solidity
  bytes32 lsp1typeIdDelegateKey = LSP2Utils.generateMappingKey(
  _LSP1_UNIVERSAL_RECEIVER_DELEGATE_PREFIX, bytes20(typeId));
```
Mapping keys are constructed of a 10-byte prefix, 2 zero bytes and a 20-byte suffix. However, 
followers of the specification will use an incorrect suffix.
The docs do not discuss the trimming of bytes32 into a bytes20 type. The mismatch may cause 
various harmful scenarios when interacting with the delegate not using the reference 
implementation.

**Recommended Mitigation:**
Document the trimming action in the LSP0 specification.

**Team Response:**
Fix applied (documented in specs).

**Mitigation review:**
Docs clearly state the described behavior.
