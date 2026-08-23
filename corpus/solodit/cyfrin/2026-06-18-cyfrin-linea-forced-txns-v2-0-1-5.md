---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-1-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: Incorrect natspec above `LineaRollupBase::_computePublicInput`
vuln_class: []
---

# Incorrect natspec above `LineaRollupBase::_computePublicInput`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** Incorrect natspec above `LineaRollupBase::_computePublicInput`:
```diff
   * 0x220   l2MerkleRootsLengthLocation
-  * 0x240   l2MessagingBlocksOffsetsLengthLocation
+  * 0x240   filteredAddressesLengthLocation
+  * 0x260   l2MessagingBlocksOffsetsLengthLocation
```

Also consider changing the name convention from "...LengthLocation" to "...OffsetPointer". The values stored at those offsets are not length locations, they're offset pointers. The offset pointer indicates where in the tail to find the length-prefixed array data:
* `calldataload(add(_finalizationData, 0x240))` returns a relative byte offset (e.g., 0x2a0)
* adding that offset to `_finalizationData` gives the length location: `add(_finalizationData, 0x2a0)` → where the array length lives
* the actual array elements start at `add(_finalizationData, 0x2c0)`

So they're offset pointers that resolve to length locations, but they aren't the length locations themselves.

**Proof of Concept:** The Foundry tests are broken; to get the PoC working first remove old evm versions from `foundry.toml`:
```solidity
[profile.default]
src = 'src'
out = 'out'
libs = ['node_modules', 'lib']
cache_path  = 'cache_forge'
foundry_version = "stable"

# Test settings
match-path = 'test/foundry/*'

# Default solc compiler settings
evm_version = "osaka"
optimizer = true
optimizer_runs = 10_000
```

Then comment out the code in `contracts/test/foundry/LineaRollup.t.sol` since it no longer compiles.

Afterwards add new PoC file `contracts/test/foundry/CalldataLayoutProof.t.sol`:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.33;

import "forge-std/Test.sol";

/**
 * @title Proof that FinalizationDataV4 NatSpec comments have wrong calldata offsets.
 * @dev The NatSpec in _computePublicInput claims:
 *        0x220   l2MerkleRootsLengthLocation
 *        0x240   l2MessagingBlocksOffsetsLengthLocation
 *
 *      But the actual ABI-encoded layout is:
 *        0x220   l2MerkleRoots offset pointer
 *        0x240   filteredAddresses offset pointer        ← MISSING from NatSpec
 *        0x260   l2MessagingBlocksOffsets offset pointer  ← NatSpec says 0x240
 *
 *      This test proves it by encoding a FinalizationDataV4 struct and inspecting
 *      the raw calldata bytes at each offset.
 */

// Minimal reproduction of the struct types
struct ShnarfData {
    bytes32 parentShnarf;
    bytes32 snarkHash;
    bytes32 finalStateRootHash;
    bytes32 dataEvaluationPoint;
    bytes32 dataEvaluationClaim;
}

struct FinalizationDataV4 {
    bytes32 parentStateRootHash;                        // 0x00
    uint256 endBlockNumber;                             // 0x20
    ShnarfData shnarfData;                              // 0x40-0xc0 (5 slots inline)
    uint256 lastFinalizedTimestamp;                     // 0xe0
    uint256 finalTimestamp;                             // 0x100
    bytes32 lastFinalizedL1RollingHash;                 // 0x120
    bytes32 l1RollingHash;                              // 0x140
    uint256 lastFinalizedL1RollingHashMessageNumber;    // 0x160
    uint256 l1RollingHashMessageNumber;                 // 0x180
    uint256 l2MerkleTreesDepth;                         // 0x1a0
    uint256 lastFinalizedForcedTransactionNumber;       // 0x1c0
    uint256 finalForcedTransactionNumber;               // 0x1e0
    bytes32 lastFinalizedForcedTransactionRollingHash;  // 0x200
    bytes32[] l2MerkleRoots;                            // 0x220 offset pointer
    address[] filteredAddresses;                        // 0x240 offset pointer
    bytes l2MessagingBlocksOffsets;                     // 0x260 offset pointer
}

contract CalldataInspector {
    /// @dev We use calldata to get the exact ABI-encoded layout that
    ///      LineaRollupBase._computePublicInput operates on.
    ///
    ///      Returns the raw 32-byte words at offsets 0x220, 0x240, 0x260
    ///      within the struct's calldata encoding.
    function inspect(
        FinalizationDataV4 calldata _data
    )
        external
        pure
        returns (
            uint256 wordAt0x220,
            uint256 wordAt0x240,
            uint256 wordAt0x260,
            // Also return the actual dynamic data to prove the offset pointers
            // resolve to the correct arrays
            uint256 merkleRootsLength,
            bytes32 merkleRootsFirstElement,
            uint256 filteredAddressesLength,
            address filteredAddressesFirstElement,
            uint256 messagingOffsetsLength
        )
    {
        assembly {
            // Read the raw 32-byte words at each offset relative to _data
            wordAt0x220 := calldataload(add(_data, 0x220))
            wordAt0x240 := calldataload(add(_data, 0x240))
            wordAt0x260 := calldataload(add(_data, 0x260))

            // Dereference offset at 0x220 → should point to l2MerkleRoots
            let merkleRootsLoc := add(_data, wordAt0x220)
            merkleRootsLength := calldataload(merkleRootsLoc)
            merkleRootsFirstElement := calldataload(add(merkleRootsLoc, 0x20))

            // Dereference offset at 0x240 → should point to filteredAddresses
            let filteredLoc := add(_data, wordAt0x240)
            filteredAddressesLength := calldataload(filteredLoc)
            filteredAddressesFirstElement := calldataload(add(filteredLoc, 0x20))

            // Dereference offset at 0x260 → should point to l2MessagingBlocksOffsets
            let messagingLoc := add(_data, wordAt0x260)
            messagingOffsetsLength := calldataload(messagingLoc)
        }
    }
}

contract CalldataLayoutProofTest is Test {
    CalldataInspector inspector;

    function setUp() public {
        inspector = new CalldataInspector();
    }

    function test_finalizationDataV4_calldata_layout() public view {
        // Build a FinalizationDataV4 with recognizable sentinel values
        // in the dynamic arrays so we can verify correct dereferencing.

        bytes32[] memory merkleRoots = new bytes32[](2);
        merkleRoots[0] = bytes32(uint256(0xAAAA));
        merkleRoots[1] = bytes32(uint256(0xBBBB));

        address[] memory filtered = new address[](1);
        filtered[0] = address(0xDEAD);

        bytes memory messagingOffsets = hex"CCDD";

        FinalizationDataV4 memory data = FinalizationDataV4({
            parentStateRootHash: bytes32(uint256(1)),
            endBlockNumber: 1000,
            shnarfData: ShnarfData({
                parentShnarf: bytes32(uint256(2)),
                snarkHash: bytes32(uint256(3)),
                finalStateRootHash: bytes32(uint256(4)),
                dataEvaluationPoint: bytes32(uint256(5)),
                dataEvaluationClaim: bytes32(uint256(6))
            }),
            lastFinalizedTimestamp: 7,
            finalTimestamp: 8,
            lastFinalizedL1RollingHash: bytes32(uint256(9)),
            l1RollingHash: bytes32(uint256(10)),
            lastFinalizedL1RollingHashMessageNumber: 11,
            l1RollingHashMessageNumber: 12,
            l2MerkleTreesDepth: 5,
            lastFinalizedForcedTransactionNumber: 13,
            finalForcedTransactionNumber: 14,
            lastFinalizedForcedTransactionRollingHash: bytes32(uint256(15)),
            l2MerkleRoots: merkleRoots,
            filteredAddresses: filtered,
            l2MessagingBlocksOffsets: messagingOffsets
        });

        (
            uint256 wordAt0x220,
            uint256 wordAt0x240,
            uint256 wordAt0x260,
            uint256 merkleRootsLength,
            bytes32 merkleRootsFirstElement,
            uint256 filteredAddressesLength,
            address filteredAddressesFirstElement,
            uint256 messagingOffsetsLength
        ) = inspector.inspect(data);

        // ──────────────────────────────────────────────────────────────────
        // PROOF 1: All three offsets at 0x220, 0x240, 0x260 are DISTINCT
        //          offset pointers (not zero, not the same value).
        //
        //          If the NatSpec were correct (only 2 dynamic fields with
        //          offsets at 0x220 and 0x240), then 0x260 would be the
        //          start of the tail data, not an offset pointer.
        // ──────────────────────────────────────────────────────────────────

        assertTrue(wordAt0x220 != wordAt0x240, "0x220 and 0x240 should be different offset pointers");
        assertTrue(wordAt0x240 != wordAt0x260, "0x240 and 0x260 should be different offset pointers");
        assertTrue(wordAt0x220 != wordAt0x260, "0x220 and 0x260 should be different offset pointers");

        // Offsets should be strictly increasing (arrays laid out in order in tail)
        assertTrue(wordAt0x220 < wordAt0x240, "l2MerkleRoots offset < filteredAddresses offset");
        assertTrue(wordAt0x240 < wordAt0x260, "filteredAddresses offset < l2MessagingBlocksOffsets offset");

        // ──────────────────────────────────────────────────────────────────
        // PROOF 2: Dereferencing offset at 0x220 yields l2MerkleRoots
        // ──────────────────────────────────────────────────────────────────

        assertEq(merkleRootsLength, 2, "0x220 -> l2MerkleRoots: length should be 2");
        assertEq(merkleRootsFirstElement, bytes32(uint256(0xAAAA)), "0x220 -> l2MerkleRoots[0] should be 0xAAAA");

        // ──────────────────────────────────────────────────────────────────
        // PROOF 3: Dereferencing offset at 0x240 yields filteredAddresses
        //          THIS IS THE FIELD MISSING FROM THE NATSPEC COMMENT.
        //          The NatSpec claims 0x240 is l2MessagingBlocksOffsets.
        // ──────────────────────────────────────────────────────────────────

        assertEq(filteredAddressesLength, 1, "0x240 -> filteredAddresses: length should be 1");
        assertEq(
            filteredAddressesFirstElement,
            address(0xDEAD),
            "0x240 -> filteredAddresses[0] should be 0xDEAD (NOT messaging offsets data)"
        );

        // ──────────────────────────────────────────────────────────────────
        // PROOF 4: Dereferencing offset at 0x260 yields l2MessagingBlocksOffsets
        //          The NatSpec says this is at 0x240, but it's actually at 0x260.
        // ──────────────────────────────────────────────────────────────────

        assertEq(messagingOffsetsLength, 2, "0x260 -> l2MessagingBlocksOffsets: length should be 2 bytes");

        // ──────────────────────────────────────────────────────────────────
        // SUMMARY:
        //   NatSpec claims:  0x220 = l2MerkleRoots, 0x240 = l2MessagingBlocksOffsets
        //   Reality:         0x220 = l2MerkleRoots, 0x240 = filteredAddresses, 0x260 = l2MessagingBlocksOffsets
        //
        //   The NatSpec is missing filteredAddresses and has l2MessagingBlocksOffsets
        //   at the wrong offset.
        // ──────────────────────────────────────────────────────────────────
    }
}
```

Run with: `forge test --match-test test_finalizationDataV4_calldata_layout`

**Linea:** Fixed in commit [857c4b7](https://github.com/Consensys/linea-monorepo/pull/2297/changes/857c4b76c90244bf8c5c8bd66c0f74726ce0cd6b#diff-99ffaedf2a0a7fba64bba5cb2ae2ad8c1587960f6cf5104f3e12f67a5c7d38d8L611-R611).

**Cyfrin:** Verified.

\clearpage
