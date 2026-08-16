---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-11
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopValidation::validateSignature` branches on `code.length`, routing EIP-7702-delegated
  EOAs to the ERC-1271 path and reverting'
vuln_class: []
---

# `BebopValidation::validateSignature` branches on `code.length`, routing EIP-7702-delegated EOAs to the ERC-1271 path and reverting

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `validateSignature` selects between ECDSA recovery and ERC-1271 contract verification by checking `validationAddress.code.length == 0` (line 58). Post-EIP-7702 (live on Ethereum mainnet since the Pectra hard fork), an EOA can set a delegation designator that gives it a non-zero `code.length` while remaining controlled by its private key. Such an EOA producing a standard 65-byte or 64-byte EIP-2098 ECDSA signature is incorrectly routed to the `else` branch, which calls `IERC1271(validationAddress).isValidSignature`. Unless the delegate's implementation happens to return the ERC-1271 magic value for the same ECDSA signature, the call reverts with `InvalidContractSignature`.

This affects all three validation call sites: `order.tokensOwner` in `settle` (line 210), hook `maker` addresses (line 372), and `routerSigner` (line 346). The affected party can recover by removing the EIP-7702 delegation, making this a recoverable denial-of-service.

**Files:**

- `contracts/base/BebopValidation.sol:58-77`

**Impact:** EIP-7702-delegated EOAs are unable to participate as `tokensOwner` in gasless settlements, as hook makers, or as the router signer until they remove their delegation. No fund loss; the affected path is blocked until the user undelegates. Impact grows as EIP-7702 adoption increases.

**Recommended Mitigation:** Attempt ECDSA recovery first for 64-byte and 65-byte inputs and only fall back to ERC-1271 if ECDSA does not recover the expected address, regardless of `code.length`. OpenZeppelin's `SignatureChecker::isValidSignatureNow` follows this pattern and handles plain EOAs, contract wallets, and EIP-7702-delegated EOAs uniformly:

```solidity
function validateSignature(address validationAddress, bytes32 hash, bytes calldata signature) public view {
    // Try ECDSA first for 64/65-byte signatures
    if (signature.length == 64 || signature.length == 65) {
        address recovered = _tryRecover(hash, signature);
        if (recovered == validationAddress) return;
    }
    // Fall back to ERC-1271
    if (validationAddress.code.length > 0) {
        bytes4 magicValue = IERC1271(validationAddress).isValidSignature(hash, signature);
        require(magicValue == EIP1271_MAGICVALUE, InvalidContractSignature());
        return;
    }
    revert InvalidSignature();
}
```

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
