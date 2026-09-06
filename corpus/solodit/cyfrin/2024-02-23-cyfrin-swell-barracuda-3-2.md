---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: '`NodeOperatorRegistry::_parsePubKeyToString`: Use shift operations rather
  than division/multiplication when dividend/factor is a power of 2'
vuln_class: []
---

# `NodeOperatorRegistry::_parsePubKeyToString`: Use shift operations rather than division/multiplication when dividend/factor is a power of 2

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** While `DIV` and `MUL` opcodes cost 5 gas unit each, shift operations cost 3 gas units. Therefore, `NodeOperatorRegistry::_parsePubKeyToString` can take advantage of them to save gas:

```diff
+   uint256 private SYMBOL_LENGTH = 16 // Because _SYMBOLS.length = 16
    function _parsePubKeyToString(
        bytes memory pubKey
    ) internal pure returns (string memory) {
        // Create the bytes that will hold the converted string
-      bytes memory buffer = new bytes(pubKey.length * 2);
+       // make sure that pubKey.length * 2 <= 2^256
+      bytes memory buffer = new bytes(pubKey.length << 1);

        bytes16 symbols = _SYMBOLS;
+       uint256 symbolLength = symbols.length;
+       uint256 index;
        for (uint256 i; i < pubKey.length; i++) {
-           buffer[i * 2] = symbols[uint8(pubKey[i]) / symbols.length];
-           buffer[i * 2 + 1] = symbols[uint8(pubKey[i]) % symbols.length];
+           index = i << 1; // i * 2
+           buffer[index] = symbols[uint8(pubKey[i]) >> 4]; // SYMBOL_LENGTH = 2^4
+           buffer[index + 1] = symbols[uint8(pubKey[i]) % SYMBOL_LENGTH];
        }

        return string(abi.encodePacked("0x", buffer));
    }
```

A more optimized version of this function looks like:
```solidity
bytes16 private constant _SYMBOLS = "0123456789abcdef";
uint256 private constant SYMBOL_LENGTH = 16; // Because _SYMBOLS.length = 16

function _parsePubKeyToString(bytes memory pubKey) internal pure returns (string memory) {
    // Create the bytes that will hold the converted string
    // make sure that pubKey.length * 2 <= 2^256
    uint256 pubKeyLength  = pubKey.length;
    bytes memory buffer   = new bytes(pubKeyLength << 1);

    uint256 index;
    for (uint256 i; i < pubKeyLength;) {
        index             = i << 1; // i * 2
        buffer[index]     = _SYMBOLS[uint8(pubKey[i]) >> 4]; // SYMBOL_LENGTH = 2^4
        buffer[index + 1] = _SYMBOLS[uint8(pubKey[i]) % SYMBOL_LENGTH];

        unchecked {++i;}
    }

    return string(abi.encodePacked("0x", buffer));
}
```

The following stand-alone test using Foundry & [Halmos](https://github.com/a16z/halmos/) verifies that the optimized version returns the same output as the original:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "forge-std/Test.sol";

// run from base project directory with:
// halmos --function test --match-contract ParseTest
contract ParseTest is Test {

    bytes16 private constant _SYMBOLS = "0123456789abcdef";
    uint256 private constant SYMBOL_LENGTH = 16; // Because _SYMBOLS.length = 16

    function _parseOriginal(bytes memory pubKey) internal pure returns (string memory) {
        // Create the bytes that will hold the converted string
        bytes memory buffer = new bytes(pubKey.length * 2);

        bytes16 symbols = _SYMBOLS;

        // This conversion relies on taking the uint8 value of each byte, the first character in the byte is the uint8 value divided by 16 and the second character is modulo of the 16 division
        for (uint256 i; i < pubKey.length; i++) {
            buffer[i * 2] = symbols[uint8(pubKey[i]) / symbols.length];
            buffer[i * 2 + 1] = symbols[uint8(pubKey[i]) % symbols.length];
        }

        return string(abi.encodePacked("0x", buffer));
    }

    function _parseOptimized(bytes memory pubKey) internal pure returns (string memory) {
        // Create the bytes that will hold the converted string
        // make sure that pubKey.length * 2 <= 2^256
        uint256 pubKeyLength  = pubKey.length;
        bytes memory buffer   = new bytes(pubKeyLength << 1);

        uint256 index;
        for (uint256 i; i < pubKeyLength;) {
            index             = i << 1; // i * 2
            buffer[index]     = _SYMBOLS[uint8(pubKey[i]) >> 4]; // SYMBOL_LENGTH = 2^4
            buffer[index + 1] = _SYMBOLS[uint8(pubKey[i]) % SYMBOL_LENGTH];

            unchecked {++i;}
        }

        return string(abi.encodePacked("0x", buffer));
    }

    function test_HalmosParse(bytes memory pubKey) public {
        string memory resultOriginal  = _parseOriginal(pubKey);
        string memory resultOptimized = _parseOptimized(pubKey);

        assertEq(resultOriginal, resultOptimized);

    }
}
```

**Swell:** Fixed in commits [7db1874](https://github.com/SwellNetwork/v3-contracts-lst/commit/7db187409c7161d981b32d639e8b925fafc431a8), [3f85df3](https://github.com/SwellNetwork/v3-contracts-lst/commit/3f85df3ba0e91b26e4234b15ad94f492fa6d46ec).

**Cyfrin:**
Verified.
