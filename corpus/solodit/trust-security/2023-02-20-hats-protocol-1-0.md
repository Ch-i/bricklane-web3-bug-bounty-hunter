---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-1 Hats token breaks ERC1155 specifications
vuln_class: []
---

# TRST-M-1 Hats token breaks ERC1155 specifications

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
The Hats token implements ERC1155 (https://eips.ethereum.org/EIPS/eip-1155). It implements safeTransferFrom() and
batchSafeTransferFrom() as revert-only functions, so tokens cannot be transferred using 
standard ERC1155 means. However, hats can still be transferred using `mintHat()`, 
`mintTopHat()` and `transferHat()`. Whenever there is a transfer, the standard requires 
checking the receiver accepts the transfer:
"If an implementation specific API function is used to transfer ERC-1155 
token(s) to a contract, the `safeTransferFrom` or `safeBatchTransferFrom` (as 
appropriate) rules MUST still be followed if the receiver implements 
the `ERC1155TokenReceiver` interface. If it does not the non-standard 
implementation SHOULD revert but MAY proceed."
By not checking a contract receiver accepts the transfer, Hats token does not adhere to 
ERC1155.

**Recommended Mitigation:**
If the recipient implements ERC1155TokenReceiver, require that it accepts the transfer. If 
the recipient is a contract that does not implement a receiver, reject the operation.

**Team Response:**
Acknowledged; changed documentation to ERC1155-similar and to explicitly clarify that Hats 
implements the ERC1155 interface but does not conform to the full standard.
