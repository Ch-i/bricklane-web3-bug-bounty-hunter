---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: Cleaner code
vuln_class: []
---

# Cleaner code

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

• Consider using the utility function `getTophatDomain()` here:
```solidity
        uint256 treeAdmin = linkedTreeAdmins[uint32(_hatId >> (256 - TOPHAT_ADDRESS_SPACE))];
```
• **SAFE_TX_TYPEHASH** is not used throughout the code, yet it is declared. Consider 
omitting it.
• Several variables which cannot be changed in the lifetime of the contract are not 
declared immutable (e.g. **maxSigners**). It wastes gas as well as potentially hurting 
the clarity of the code.
