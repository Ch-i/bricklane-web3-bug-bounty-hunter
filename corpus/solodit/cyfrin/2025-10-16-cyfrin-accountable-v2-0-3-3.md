---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: '`Authorizable::_verify` should use EIP-712 typed structured data hashing'
vuln_class: []
---

# `Authorizable::_verify` should use EIP-712 typed structured data hashing

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** [`Authorizable::_verify`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/access/Authorizable.sol#L46-L78) signs ad-hoc payloads that include `chainId`, but the flow is not [EIP-712](https://eips.ethereum.org/EIPS/eip-712) typed-data compliant. This limits wallet UX/visibility and interoperability and mixes domain data (`chainId`) with message data.

**Impact:** Users are more susceptible to ambiguous signing prompts; weaker ecosystem compatibility; harder audits/upgrades; higher risk of encoding/packing mistakes and replay bugs across contracts or chains.

**Recommended mitigation:**
Adopt EIP-712 and move `chainId` to the domain separator (remove it from the struct). Keep the existing intent of the message:

* **Domain:** `{ name: "Authorizable", version: "1", chainId, verifyingContract: address(this) }`.
* **Typed struct (no chainId inside):**

  ```solidity
  struct TxAuthData {
      bytes   functionCallData;   // selector + encoded args
      address contractAddress;    // target contract (can be redundant with domain; decide and document)
      address account;            // controller / signer subject
      uint256 nonce;              // per-account nonce
      uint256 blockExpiration;    // deadline
  }

  bytes32 constant TXAUTH_TYPEHASH = keccak256(
      "TxAuthData(bytes functionCallData,address contractAddress,address account,uint256 nonce,uint256 blockExpiration)"
  );
  ```
* **Hashing & verify (using OZ EIP712 + SignatureChecker):**

  ```solidity
  bytes32 structHash = keccak256(abi.encode(
      TXAUTH_TYPEHASH,
      keccak256(txAuth.functionCallData), // hash dynamic bytes
      txAuth.contractAddress,
      txAuth.account,
      txAuth.nonce,
      txAuth.blockExpiration
  ));
  bytes32 digest = _hashTypedDataV4(structHash);
  require(
      SignatureChecker.isValidSignatureNow(signer, digest, signature),
      "INVALID_SIGNATURE"
  );
  ```
**Accountable:** Fixed in commit [`70cd486`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/70cd4863e3bef0f80f2eeb012c79a801c099fc7e)

**Cyfrin:** Verified. EIP-712 typed data is now used for the signatures.
