---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-27-cyfrin-atum-tron-contracts-v2-1-2-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md
tags:
- firm:cyfrin
- report:2025-08-27-cyfrin-atum-tron-contracts-v2-1
title: TIP-712 requires addresses to be cast to `uint160` but `address` in TRON Solidity
  doesn't store the prefix so casting is unnecessary
vuln_class: []
---

# TIP-712 requires addresses to be cast to `uint160` but `address` in TRON Solidity doesn't store the prefix so casting is unnecessary

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-27-cyfrin-atum-tron-contracts-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md)_

---

**Description:** [TIP-712](https://github.com/tronprotocol/tips/blob/master/tip-712.md) requires addresses used in TIP-712 to be cast to `uint160`:

> * address: need to remove TRON unique prefix(0x41) and encoded as uint160
>
> The encoding of a struct instance is enc(value₁) ‖ enc(value₂) ‖ … ‖ enc(valueₙ), i.e. the concatenation of the encoded member values in the order that they appear in the type. Each encoded member value is exactly 32-byte long.
>
> It's totaly compatible with EIP-712.
>
> The only difference between TRON address and Ethereum address is that TRON address starts with a byte prefix 0x41 and uses base58 encoding, so prefix needs to be removed when the address type is processed.

However `address` in TRON Solidity is already 20 bytes without any prefix, therefore casting `address` to `uint160` wouldn't _"remove TRON unique prefix"_ - it wouldn't do anything except increase transaction costs.

**Recommended Mitigation:** * In `tvm-contracts`, the following `uint160(address)` casts can be safely removed:
```solidity
TIP712.sol
45:        return keccak256(abi.encode(typeHash, nameHash, versionHash, chainId, uint160(address(this))));
```

* In `permit2-tron`, the following `uint160(address)` casts can be safely removed:
```solidity
TIP712.sol
38:        return keccak256(abi.encode(typeHash, nameHash, chainId, uint160(address(this))));

libraries/PermitHash.sol
40:            abi.encode(_PERMIT_SINGLE_TYPEHASH, permitHash, uint160(permitSingle.spender), permitSingle.sigDeadline)
54:                uint160(permitBatch.spender),
64:                _PERMIT_TRANSFER_FROM_TYPEHASH, tokenPermissionsHash, uint160(msg.sender), permit.nonce, permit.deadline
81:                uint160(msg.sender),
97:            abi.encode(typeHash, tokenPermissionsHash, uint160(msg.sender), permit.nonce, permit.deadline, witness)
120:                uint160(msg.sender),
132:                _PERMIT_DETAILS_TYPEHASH, uint160(details.token), details.amount, details.expiration, details.nonce
143:        return keccak256(abi.encode(_TOKEN_PERMISSIONS_TYPEHASH, uint160(permitted.token), permitted.amount));
```

The only time a `uint160` cast makes sense is if an address is passed as external input using `bytes` or `uint256` and it also contains the `TRON` prefix.

**Atum:**
Fixed in commit [e0b9ce3](https://github.com/alexroan/permit2-tron/commit/e0b9ce3163443013cf83027ca58457c80e8dc86c) for `permit2-tron` and commit [0772f28](https://github.com/Atum-Labs/tvm-contracts/commit/0772f285435f65900b74cd8b9cbc6cddec079dbd) for `tvm-contracts`.

**Cyfrin:** Verified.
