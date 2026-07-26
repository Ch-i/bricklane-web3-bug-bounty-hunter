---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-12
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnChainLab::isValidSignature` return `0` instead of `0xffffffff` for invalid
  signatures'
vuln_class: []
---

# `OnChainLab::isValidSignature` return `0` instead of `0xffffffff` for invalid signatures

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `OnChainLab::isValidSignature` is designed to comply with `ERC1271` signing. According to `EIP1271`, the implementation is designed to return `0xffffffff` in invalid signatures. This is how it is implemented by popular libs like OpenZeppelin.

In the current implementation, we are returning `bytes4(0x)` instead of `0xffffffff`, which is not the common return value for an invalid signature according to `EIP1271`.

> src/OnChainLab.sol#isValidSignature
```solidity
    function isValidSignature(bytes32 hash, bytes calldata signature) ... {
        // Try ERC-7739's nested EIP-712 validation first (for security)
        // 7739 provides enhanced crosschain replay protection, which is key for crosschain Labs.
        bytes4 erc7739Result = ERC7739.isValidSignature(hash, signature);

        // If ERC7739 returns invalid (0xffffffff), fall back to simple ECDSA
        // This allows backward compatibility with simple signatures
        if (erc7739Result == bytes4(0xffffffff)) {
            bool isValid = SignatureChecker.isValidSignatureNow(owner(), hash, signature);
>>          return isValid ? IERC1271.isValidSignature.selector : bytes4(0);
        }

        // Return ERC7739's result (valid, invalid, or detection magic value 0x77390001)
        return erc7739Result;
    }
```


**Recommended Mitigation:** We should represent invalid `EIP1271` signing by returning `0xffffffff` instead of `bytes4(0)`

**Molecule:** Fixed in [6a89176](https://github.com/moleculeprotocol/onchainlabs/commit/6a89176).

**Cyfrin:** Verified.

\clearpage
