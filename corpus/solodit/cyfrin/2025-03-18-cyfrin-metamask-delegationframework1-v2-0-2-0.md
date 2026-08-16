---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: '`EIP7702StatelessDeleGator` violates `EIP4337` signature validation standards'
vuln_class: []
---

# `EIP7702StatelessDeleGator` violates `EIP4337` signature validation standards

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** The `EIP7702StatelessDeleGator` implementation doesn't properly adhere to the EIP4337 standard regarding signature validation behavior.

According to EIP4337, the `validateUserOp` method should:

1. Return SIG_VALIDATION_FAILED (without reverting) only for signature mismatch cases
2. Revert for any other errors (including invalid signature format, incorrect length)

The current implementation in `EIP7702StatelessDeleGator._isValidSignature()` returns `SIG_VALIDATION_FAILED` for both signature mismatches and invalid signature length, which violates the specification:

```solidity
// EIP7702StatelessDeleGator.sol
    function _isValidSignature(bytes32 _hash, bytes calldata _signature) internal view override returns (bytes4) {
>>      if (_signature.length != SIGNATURE_LENGTH) return ERC1271Lib.SIG_VALIDATION_FAILED;

        if (ECDSA.recover(_hash, _signature) == address(this)) return ERC1271Lib.EIP1271_MAGIC_VALUE;

        return ERC1271Lib.SIG_VALIDATION_FAILED;
    }
```

This implementation is used by the `EntryPoint` when validating `UserOperations`, and incorrect handling can lead to inconsistencies with other EIP4337-compliant wallets.

**Impact:** Creates potential inconsistency with other EIP4337-compliant wallets

**Recommended Mitigation:** Consider removing the signature length check in `EIP7702StatelessDeleGator._isValidSignature()`. This will cause the function to rely on OpenZeppelin's `ECDSA.recover()` function to revert for invalid signature formats, consistent with the EIP4337 specification.

**Metamask**
Fixed in [b52cf04](https://github.com/MetaMask/delegation-framework/commit/b52cf041f5a41914d9014d777da9a3db17080fa6).

**Cyfrin**
Resolved.
