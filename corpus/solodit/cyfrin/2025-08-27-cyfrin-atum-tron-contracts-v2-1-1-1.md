---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-27-cyfrin-atum-tron-contracts-v2-1-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md
tags:
- firm:cyfrin
- report:2025-08-27-cyfrin-atum-tron-contracts-v2-1
title: Smart contract wallets using Approved Hashes are limited to one active deposit
  at a time
vuln_class: []
---

# Smart contract wallets using Approved Hashes are limited to one active deposit at a time

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-27-cyfrin-atum-tron-contracts-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md)_

---

**Description:** `Escrow::deposit` generates the unique `depositId` based on the depositor's address and their signature:
```solidity
depositId = keccak256(abi.encode(depositor, signature));
```

The problem in this is that the signature is always `65/64` length for EOA wallets, but it can be with different values in case of Smart Contract Wallets.

Some Smart Contract Wallets like Safe Wallet have a concept of `Approved Hashes` where the owners of the wallet can approve a given hash, then after signing the hash it is moved to `Approved hashes` mapping or it can be approved before that.

The problem is that in order to use the Approved Hashes feature you should pass signature of zero length, so as to let the verification go through Approved Hash:
[SafeWallet::SignatureVerifierMuxer.sol#L154-L156](https://github.com/safe-global/safe-smart-account/blob/024f544092f0a9635781617a35d8c3342a76f01a/contracts/handler/extensible/SignatureVerifierMuxer.sol#L154-L156)
```solidity
    function defaultIsValidSignature(ISafe safe, bytes32 _hash, bytes memory signature) internal view returns (bytes4 magic) {
        bytes memory messageData = EIP712.encodeMessageData(
            safe.domainSeparator(),
            SAFE_MSG_TYPEHASH,
            abi.encode(keccak256(abi.encode(_hash)))
        );
        bytes32 messageHash = keccak256(messageData);
>>      if (signature.length == 0) {
            // approved hashes
>>          require(safe.signedMessages(messageHash) != 0, "Hash not approved");
        } else {
            // threshold signatures
            safe.checkSignatures(address(0), messageHash, signature);
        }
>>      magic = ERC1271.isValidSignature.selector;
    }
```

So in order for Smart Contract wallets relying on Approved Hashes, they will provide signature of zero length. In the case they have an active deposit, they will be prevented from making another deposit unless the old one gets completed (released/refunded), limited users to one active deposit.

**Impact:** Users of Smart Contract wallets using approved hashes are limited to one active deposit.

**Recommended Mitigation:** In `Escrow::deposit` also use `permit.nonce` when generating `depositId`.

**Atum:**
Acknowledged; will be fixed in a future version.

\clearpage
