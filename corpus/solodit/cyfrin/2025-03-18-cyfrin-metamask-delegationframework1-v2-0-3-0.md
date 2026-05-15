---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: DelegationManager is incompatible with smart contract wallets with Approved
  hashes
vuln_class: []
---

# DelegationManager is incompatible with smart contract wallets with Approved hashes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** In the `DelegationManager` contract, there is a limitation that affects smart contract wallets that implement pre-approved hashes functionality, such as Safe (formerly Gnosis Safe) wallets. The current implementation rejects delegations with empty signatures for both EOA and smart contract wallets.

```solidity
// DelegationManager.sol
    function redeemDelegations( ... ) ... {
        ...
        for (uint256 batchIndex_; batchIndex_ < batchSize_; ++batchIndex_) {
            ...
            if (delegations_.length == 0) { ... } else {
                ...
                for (uint256 delegationsIndex_; delegationsIndex_ < delegations_.length; ++delegationsIndex_) {
                    ...
>>                  if (delegation_.signature.length == 0) {
                        // Ensure that delegations without signatures revert
                        revert EmptySignature();
                    }

                    if (delegation_.delegator.code.length == 0) {
                        // Validate delegation if it's an EOA
                        ...
                    } else {
                        // Validate delegation if it's a contract
                        ...
>>                      bytes32 result_ = IERC1271(delegation_.delegator).isValidSignature(typedDataHash_, delegation_.signature);
                        ...
                    }
                }
```

This presents a compatibility issue with Safe wallets and similar smart contract wallets that use a pattern where empty signatures trigger checking for pre-approved hashes. In Safe's implementation:

[SignatureVerifierMuxer.sol#L163-L165](https://github.com/safe-global/safe-smart-account/blob/main/contracts/handler/extensible/SignatureVerifierMuxer.sol#L163-L165)
```solidity
    function isValidSignature(bytes32 _hash, bytes calldata signature) external view override returns (bytes4 magic) {
        (ISafe safe, address sender) = _getContext();

        // Check if the signature is for an `ISafeSignatureVerifier` and if it is valid for the domain.
        if (signature.length >= 4) {
            ...

            // Guard against short signatures that would cause abi.decode to revert.
            if (sigSelector == SAFE_SIGNATURE_MAGIC_VALUE && signature.length >= 68) { ... }
        }

        // domainVerifier doesn't exist or the signature is invalid for the domain - fall back to the default
>>      return defaultIsValidSignature(safe, _hash, signature);
    }
// -----------------
    function defaultIsValidSignature(ISafe safe, bytes32 _hash, bytes memory signature) internal view returns (bytes4 magic) {
        bytes memory messageData = EIP712.encodeMessageData( ... );
        bytes32 messageHash = keccak256(messageData);
>>      if (signature.length == 0) {
            // approved hashes
>>          require(safe.signedMessages(messageHash) != 0, "Hash not approved");
        } else {
            // threshold signatures
            safe.checkSignatures(address(0), messageHash, signature);
        }
        magic = ERC1271.isValidSignature.selector;
    }
```

Since DelegationManager rejects empty signatures before calling `isValidSignature`, it prevents Safe wallets from using their pre-approved hash mechanism for delegations.

**Impact:** This limitation prevents Safe wallets and similar smart contract wallets from using their gas-efficient pre-approved hash mechanism with delegations.

**Recommended Mitigation:** To enable compatibility with Safe wallets' pre-approved hash mechanism, consider applying the empty signature check only to EOAs. Alternatively, consider documenting that Safe wallets pre-approved hashes are not supported in the current delegation framework.

**Metamask:** Fixed in commit [155d20c](https://github.com/MetaMask/delegation-framework/commit/155d20c8bf173d556ef738ec808b3583da1a7c9d).

**Cyfrin:** Resolved.
