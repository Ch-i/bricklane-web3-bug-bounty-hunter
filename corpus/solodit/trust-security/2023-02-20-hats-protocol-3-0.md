---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: Documentation issues
vuln_class: []
---

# Documentation issues

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

• Remove irrelevant comment in `buildHatId()`:
```solidity///
        @dev Check hats[_admin].lastHatId for the previous hat created underneath _admin
 ```
• Correct comment in checkHatStatus():
```solidity
        // then we know the contract exists and has the getWearerStatus function
```
• Remove comment in MultiHatsSignerGate's claimSigner():
```solidity
        /// @dev overloads HatsSignerGateBase.claimSigner()
```
• Change comment in approveLinkTopHatToTree() – can be approved by wearer or
admin
```solidity
        /// @dev Requests can only be approved by an admin of the `_newAdminHat`, and there
```
