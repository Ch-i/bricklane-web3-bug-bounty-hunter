---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: '`LibLastReserveBytes::storeLastReserves` has no check for reserves being too
  large'
vuln_class: []
---

# `LibLastReserveBytes::storeLastReserves` has no check for reserves being too large

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

**Description:** After every liquidity event & swap, the `IPump::update`()` is called.
To update the pump, the `LibLastReserveBytes::storeLastReserves` function is used. This packs the reserve data into `bytes32` slots in storage.
A slot is then broken down into the following components:
- 1 byte for reserves array length
- 5 bytes for `timestamp`
- 16 bytes for each reserve balance

This adds to 22 bytes total, but the function also attempts to pack the second reserve balance in the `bytes32` object.
This would mean the `bytes32` would need 38 bytes total:

`1(length) + 5(timestamp) + 16(reserve balance 1) + 16(reserve balance 2) = 38 bytes`

To fit all this data into the `bytes32`, the function cuts off the last few bytes of the reserve balances using shift, as shown below.

```solidity
src\libraries\LibLastReserveBytes.sol
21:    uint8 n = uint8(reserves.length);
22:    if (n == 1) {
23:        assembly {
24:            sstore(slot, or(or(shl(208, lastTimestamp), shl(248, n)), shl(104, shr(152, mload(add(reserves, 32))))))
25:        }
26:        return;
27:    }
28:    assembly {
29:        sstore(
30:            slot,
31:            or(
32:                or(shl(208, lastTimestamp), shl(248, n)),
33:                or(shl(104, shr(152, mload(add(reserves, 32)))), shr(152, mload(add(reserves, 64))))
34:            )
35:        )
36:        // slot := add(slot, 32)
37:    }
```

So if the amount being stored is too large, the actual stored value will be different than what was expected to be stored.

On the other hand, the `LibBytes.sol` does seem to have a check:
```solidity
require(reserves[0] <= type(uint128).max, "ByteStorage: too large");
```
The `_setReserves` function calls this library after every reserve update in the well.
So in practice, with the currently implemented wells & pumps, this check would cause a revert.

However, a well that is implemented without this check could additionally trigger the pumps to cut off reserve data, meaning prices would be incorrect.

**Impact:** While we assume users will be explicitly warned about malicious Wells and are unlikely to interact with invalid Wells, we assess the severity to be MEDIUM.

**Proof of Concept:**
```solidity
function testStoreAndReadTwo() public {
    uint40 lastTimeStamp = 12345363;
    bytes16[] memory reserves = new bytes16[](2);
    reserves[0] = 0xffffffffffffffffffffffffffffffff; // This is too big!
    reserves[1] = 0x11111111111111111111111100000000;
    RESERVES_STORAGE_SLOT.storeLastReserves(lastTimeStamp, reserves);
    (
        uint8 n,
        uint40 _lastTimeStamp,
        bytes16[] memory _reserves
    ) = RESERVES_STORAGE_SLOT.readLastReserves();
    assertEq(2, n);
    assertEq(lastTimeStamp, _lastTimeStamp);
    assertEq(reserves[0], _reserves[0]); // This will fail
    assertEq(reserves[1], _reserves[1]);
    assertEq(reserves.length, _reserves.length);
}
```

**Recommended Mitigation:** We recommend adding a check on the size of reserves in `LibLastReseveBytes`.

Additionally, it is recommended to add comments to `LibLastReseveBytes` to inform users about the invariants of the system and how the max size of reserves should be equal to the max size of a `bytes16` and not a `uint256`.

**Beanstalk:** Because the Pump packs 2 last reserve values in the form of `bytes16` quadruple precision floating point values and a `uint40` timestamp into the same slot, there is a loss of precision on last reserve values. Each last reserve value only has precision of ~27 decimals instead of the expected ~34 decimals.

Given that the last reserves are only used to determine the cap on reserve updates and that the 27 decimals that are preserved are the most significant decimals, the impact due to this is minimal. The cap is only used to prevent the effect of manipulation, and is arbitrarily set. It is also never evaluated by external protocols. Finally, 27 decimal precision is still quite significant → If would need to be about 1,000,000,000,000,000,000,000,000,000 tokens in the pool for there to be an error of 1.

**Cyfrin:** Acknowledged.

\clearpage
