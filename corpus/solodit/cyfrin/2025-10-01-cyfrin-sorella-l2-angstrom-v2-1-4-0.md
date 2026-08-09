---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-4-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Unnecessary inline assembly operations can be removed and replaced by hardcoded
  constants
vuln_class: []
---

# Unnecessary inline assembly operations can be removed and replaced by hardcoded constants

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `PoolKeyHelperLib::calldataToId` currently performs two unnecessary `mul` operations in computing the slice length:

```solidity
function calldataToId(PoolKey calldata poolKey) internal pure returns (PoolId id) {
    assembly ("memory-safe") {
        let ptr := mload(0x40)
@>      calldatacopy(ptr, poolKey, mul(32, 5))
@>      id := keccak256(ptr, mul(32, 5))
    }
}
```

Instead, these operations can be avoided by referencing the length of 160 bytes directly.

Similarly, `PoolRewards::getPosition` currently performs three unnecessary `add` operations:

```solidity
positionKey := keccak256(12, add(add(3, 3), add(20, 32)))
```

Instead, these operations can be avoided by referencing the the length of 58 bytes directly.

**Recommended Mitigation:**
```diff
// PoolKeyHelperLib.sol
function calldataToId(PoolKey calldata poolKey) internal pure returns (PoolId id) {
    assembly ("memory-safe") {
        let ptr := mload(0x40)
-       calldatacopy(ptr, poolKey, mul(32, 5))
-       id := keccak256(ptr, mul(32, 5))
+       calldatacopy(ptr, poolKey, 160)
+       id := keccak256(ptr, 160)
    }
}

// PoolRewards.sol
function getPosition(
    PoolRewards storage self,
    address owner,
    int24 lowerTick,
    int24 upperTick,
    bytes32 salt
) internal view returns (Position storage position, bytes32 positionKey) {
    assembly ("memory-safe") {
        // Compute Uniswap position key `keccak256(abi.encodePacked(owner, lowerTick, upperTick, salt))`.
        mstore(0x06, upperTick)
        mstore(0x03, lowerTick)
        mstore(0x00, owner)
        // WARN: Free memory pointer temporarily invalid from here on.
        mstore(0x26, salt)
-       positionKey := keccak256(12, add(add(3, 3), add(20, 32)))
+       positionKey := keccak256(12, 58)
        // Upper bytes of free memory pointer cleared.
        mstore(0x26, 0)
    }
    position = self.positions[positionKey];
}
```

**Sorella Labs:** Acknowledged. I left these as explicit adds to make it more explicit where the constant comes from, the compiler should trivially fold this into a constant anyway at compile time.

**Cyfrin:** Acknowledged.
