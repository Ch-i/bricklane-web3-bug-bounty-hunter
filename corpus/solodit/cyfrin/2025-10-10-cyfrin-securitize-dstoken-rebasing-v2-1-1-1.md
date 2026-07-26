---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Incorrect EIP-712 `TXTYPE_HASH` in `SecuritizeSwap`
vuln_class: []
---

# Incorrect EIP-712 `TXTYPE_HASH` in `SecuritizeSwap`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `SecuritizeSwap::TXTYPE_HASH` does not match the actual message structure being encoded for EIP-712 signature verification. The constant is defined as the hash of:
```solidity
"ExecutePreApprovedTransaction(string memory _senderInvestor, address _destination,address _executor,bytes _data, uint256[] memory _params)"
```

But the actual `abi.encode` call in `SecuritizeSwap::doExecuteByInvestor` encodes a different structure:

```solidity
function doExecuteByInvestor(
        uint8 _securitizeHsmSigV,
        bytes32 _securitizeHsmSigR,
        bytes32 _securitizeHsmSigS,
        string memory _senderInvestorId,
        address _destination,
        bytes memory _data,
        address _executor,
        uint256[] memory _params
    ) internal {
        bytes32 txInputHash = keccak256(
            abi.encode(
                TXTYPE_HASH,
                _destination,
                _params[0], //value
                keccak256(_data),
                noncePerInvestor[_senderInvestorId],
                _executor,
                _params[1], //gasLimit
                keccak256(abi.encodePacked(_senderInvestorId))
            )
        );
        ...
    }
```

The type string declares 5 parameters in this order:

1) string _senderInvestor
2) address _destination
3) address _executor
4) bytes _data
5) uint256[] _params

But the actual encoding has 7 parameters:

1) address destination
2) uint256 value (from params[0])
3) bytes32 dataHash (keccak of _data)
4) uint256 nonce
5) address executor
6) uint256 gasLimit (from params[1])
7) bytes32 investorIdHash (keccak of _senderInvestor)

This is a significant mismatch between the expected message type and the actual encoded parameters that violates EIP-712 structured data standards.

Another problem is that the EIP-712 spec does not have storage qualifiers like `storage` and `memory` in the type hash string. So even if the above mismatch didn't occur, the current hash is still incorrect as it has been created using an incorrect type hash string.

**Impact:** The implementation violates EIP-712 standards which could cause compatibility issues with wallets and signing tools that expect proper EIP-712 compliance.

**Recommended Mitigation:** Correct `TXTYPE_HASH`:
* remove `memory` keyword from type hash string
* change type hash string to match the actual encoded parameters
* generate a new hash using the corrected type hash string

A potential fix looks like:
```solidity
// keccak256("ExecutePreApprovedTransaction(address destination,uint256 value,bytes32 data,uint256 nonce,address executor,uint256 gasLimit,bytes32 investorIdHash)")
bytes32 constant TXTYPE_HASH = 0xf13da213cea16aa5bb997703966334f85e5aa4d2b25964a7191e3a7bc08b7690;
```

**Securitize:** `SecuritizeSwap` was removed as it was deprecated.

**Cyfrin:** Verified.
