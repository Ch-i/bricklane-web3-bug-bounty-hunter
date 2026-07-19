---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Incorrect sload in LibBytes
vuln_class: []
---

# Incorrect sload in LibBytes

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

**Description:** The function `storeUint128` in `LibBytes` intends to pack uint128 `reserves` starting at the given slot but will overwrite the final slot if [storing an odd number of reserves](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/libraries/LibBytes.sol#L70). It is currently only ever called in [`Well::_setReserves`](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/Well.sol#L609) which takes as input the result of `Well::_updatePumps` which itself always takes `_tokens.length` as an argument. Hence, in the case of an odd number of tokens, the final 128 bits in the slot are never accessed, regardless of the error. However, there may be a case in which the library is used by other implementations, setting a variable number of reserves at any one time rather than always acting on the length of tokens, which may inadvertently overwrite the final reserve to zero.

**Impact:** Given assets are not directly at risk, we evaluate the severity to LOW.

**Proof of Concept:** The following test case demonstrates this issue more clearly:

```solidity
// NOTE: Add to LibBytes.t.sol
function test_exploitStoreAndRead() public {
    // Write to storage slot to demonstrate overwriting existing values
    // In this case, 420 will be stored in the lower 128 bits of the last slot
    bytes32 slot = RESERVES_STORAGE_SLOT;
    uint256 maxI = (NUM_RESERVES_MAX - 1) / 2;
    uint256 storeValue = 420;
    assembly {
        sstore(add(slot, mul(maxI, 32)), storeValue)
    }

    // Read reserves and assert the final reserve is 420
    uint[] memory reservesBefore = LibBytes.readUint128(RESERVES_STORAGE_SLOT, NUM_RESERVES_MAX);
    emit log_named_array("reservesBefore", reservesBefore);

    // Set up reserves to store, but only up to NUM_RESERVES_MAX - 1 as we have already stored a value in the last 128 bits of the last slot
    uint[] memory reserves = new uint[](NUM_RESERVES_MAX - 1);
    for (uint i = 1; i < NUM_RESERVES_MAX; i++) {
        reserves[i-1] = i;
    }

    // Log the last reserve before the store, perhaps from other implementations which don't always act on the entire reserves length
    uint256 t;
    assembly {
        t := shr(128, shl(128, sload(add(slot, mul(maxI, 32)))))
    }
    emit log_named_uint("final slot, lower 128 bits before", t);

    // Store reserves
    LibBytes.storeUint128(RESERVES_STORAGE_SLOT, reserves);

    // Re-read reserves and compare
    uint[] memory reserves2 = LibBytes.readUint128(RESERVES_STORAGE_SLOT, NUM_RESERVES_MAX);

    emit log_named_array("reserves", reserves);
    emit log_named_array("reserves2", reserves2);

    // But wait, what about the last reserve
    assembly {
        t := shr(128, shl(128, sload(add(slot, mul(maxI, 32)))))
    }

    // Turns out it was overwritten by the last store as it calculates the sload incorrectly
    emit log_named_uint("final slot, lower 128 bits after", t);
}
```

Output before mitigation:

```
reservesBefore: [0, 0, 0, 0, 0, 0, 0, 420]
final slot, lower 128 bits before: 420
reserves: [1, 2, 3, 4, 5, 6, 7]
reserves2: [1, 2, 3, 4, 5, 6, 7, 0]
final slot, lower 128 bits after: 0
```

**Recommended Mitigation:** Implement the following fix to load the existing value from storage and pack in the lower bits:

```solidity
	sload(add(slot, mul(maxI, 32)))
```

Output after mitigation:

```
reservesBefore: [0, 0, 0, 0, 0, 0, 0, 420]
final slot, lower 128 bits before: 420
reserves: [1, 2, 3, 4, 5, 6, 7]
reserves2: [1, 2, 3, 4, 5, 6, 7, 420]
final slot, lower 128 bits after: 420
```

**Beanstalk:** Fixed in commit [5e61420](https://github.com/BeanstalkFarms/Basin/pull/71/commits/5e614205a49f1388c36b2a02ce38cf0df317dfde).

**Cyfrin:** Acknowledged.

\clearpage
