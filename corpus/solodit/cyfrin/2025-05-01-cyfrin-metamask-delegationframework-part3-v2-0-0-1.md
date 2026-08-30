---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-01-cyfrin-metamask-delegationframework-part3-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-05-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-01-cyfrin-metamask-delegationframework-part3-v2-0
title: Ambiguous expiration timestamp validation in `DelegationMetaSwapAdapter`
vuln_class: []
---

# Ambiguous expiration timestamp validation in `DelegationMetaSwapAdapter`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md)_

---

**Description:** In the DelegationMetaSwapAdapter.sol contract, the _validateSignature() method uses a "greater than" (>) comparison instead of a "greater than or equal to" (>=) comparison when validating signature expiration:

```solidity
function _validateSignature(SignatureData memory _signatureData) private view {
    if (block.timestamp > _signatureData.expiration) revert SignatureExpired();

    bytes32 messageHash_ = keccak256(abi.encodePacked(_signatureData.apiData, _signatureData.expiration));
    bytes32 ethSignedMessageHash_ = MessageHashUtils.toEthSignedMessageHash(messageHash_);

    address recoveredSigner_ = ECDSA.recover(ethSignedMessageHash_, _signatureData.signature);
    if (recoveredSigner_ != swapApiSigner) revert InvalidApiSignature();
}
```

This implementation allows signatures to remain valid at the exact moment of their expiration timestamp, which creates ambiguity in the intended security model.

**Impact:** A signature marked as expired (with an expiration timestamp equal to the current block timestamp) is still considered valid, which may be counter-intuitive and could lead to confusion.

**Recommended Mitigation:** If the current behavior is intentional, consider renaming the `expiration` field to `validUpto`. Alternatively, to make it semantically clear with the term `expiration`, consider replacing `>` with `>=`.

**Metamask:** Resolved in commit [6912e73](https://github.com/MetaMask/delegation-framework/commit/6912e732e2ed65699152c6bfdb46a0ed433f1263).

**Cyfrin:** Resolved.

\clearpage
