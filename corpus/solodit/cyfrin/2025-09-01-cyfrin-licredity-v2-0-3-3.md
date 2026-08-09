---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Erroneous packing in `Licredity::_calculateLiquidityKey`
vuln_class: []
---

# Erroneous packing in `Licredity::_calculateLiquidityKey`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description.**
The contract creates a “liquidity key” (the ID used to track when an LP added liquidity) with custom bit-twiddling instead of the usual `keccak256(abi.encodePacked(provider, tickLower, tickUpper, salt))` in [`Licredity::_calculateLiquidityKey`](https://github.com/Licredity/licredity-v1-core/blob/e8ae10a7d9f27529e39ca277bf56cef01a807817/src/Licredity.sol#L880-L885)
```solidity
assembly ("memory-safe") {
    // key = keccak256(abi.encodePacked(provider, tickLower, tickUpper, salt));
    mstore(0x00, or(or(shl(0x06, provider), shl(0x03, tickLower)), tickUpper))
    mstore(0x20, salt)
    key := keccak256(0x06, 0x3a)
}
```

However, it skips the first 6 bytes of the provider address and packs the tick values differently from standard ABI rules. Practically, that means:

* The key you get here won’t match what off-chain tools (or other contracts) would compute from the same inputs using normal ABI packing.
* In extremely rare cases, two different providers could land on the same key for the same ticks+salt (e.g., addresses that only differ in their first few bytes), so they would share the same “onset” slot.

**Impact.**
If two parties collide on a key, one could update the shared `liquidityOnsets[key]` and effectively reset the other party’s minimum-lifespan timer, briefly delaying their ability to remove liquidity. There’s no direct profit, finding such a collision is expensive, and liquidity below tick 0 is already discouraged by the swap guard.

**Proof of Concept:** Make `_calculateLiquidityKey` public and run this test:
```solidity
function test_calculateLiquidityKey() public view {
    address ad = address(0x1234);
    int24 tL = -1;
    int24 tH = 1;
    bytes32 salt = "";
    bytes32 key1 = licredity._calculateLiquidityKey(ad,tL,tH,salt);
    bytes32 key2 = keccak256(abi.encodePacked(ad, tL, tH, salt));
    assertEq(key1, key2);
}
```

**Recommended Mitigation:** Correctly mask and use 46 and 24 in the shifts:
```solidity
assembly ("memory-safe") {
    // key = keccak256(abi.encodePacked(provider, tickLower, tickUpper, salt));
    // Byte-aligned shifts and masks.
    let addr := and(provider, 0x000000000000000000000000ffffffffffffffffffffffffffffffffffffffff) // 20B
    let tl   := and(tickLower,  0xFFFFFF) // 3B two's complement
    let tu   := and(tickUpper,  0xFFFFFF) // 3B

    // [ 20B addr | 3B tl | 3B tu | (6B zero padding) ] in the 32B word,
    // so the slice from 0x06 of length 58 is exactly 20+3+3 + 32 salt bytes.
    let word := or(or(shl(48, addr), shl(24, tl)), tu) // 48 bits = 6 bytes, 24 bits = 3 bytes
    mstore(0x00, word)
    mstore(0x20, salt)
    key := keccak256(0x06, 0x3a)
}
```

**Licredity:** Fixed in [PR#76](https://github.com/Licredity/licredity-v1-core/pull/76/files), commit [`a5d9846`](https://github.com/Licredity/licredity-v1-core/commit/a5d98462f70a31e070941730b397c060244b3f8f)

**Cyfrin:** Verified. tick bits now cleaned as well as offsets 48 and 24 are used.

\clearpage
