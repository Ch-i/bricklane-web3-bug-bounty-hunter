---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-9
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Remove TODO Check if bytes shift is necessary
vuln_class: []
---

# Remove TODO Check if bytes shift is necessary

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

In `LibBytes16::readBytes16`, the following line has a `TODO`:

```mstore(add(reserves, 64), shl(128, sload(slot))) // TODO: Check if byte shift is necessary```

Since two reserve elements' worth of data is stored in a single slot, the left shift is indeed needed. The following test shows how these are different:

```solidity
function testNeedLeftShift() public {
    uint256 reservesSize = 2;
    uint256 slotNumber = 12345;
    bytes32 slot = bytes32(slotNumber);

    bytes16[] memory leftShiftreserves = new bytes16[](reservesSize);
    bytes16[] memory noShiftreserves = new bytes16[](reservesSize);

    // store some data in the slot
    assembly {
        sstore(
            slot,
            0x0000000000000000000000000000007b00000000000000000000000000000011
        )
    }

    // left shift
    assembly {
        mstore(add(leftShiftreserves, 32), sload(slot))
        mstore(add(leftShiftreserves, 64), shl(128, sload(slot)))
    }

    // no shift
    assembly {
        mstore(add(noShiftreserves, 32), sload(slot))
        mstore(add(noShiftreserves, 64), sload(slot))
    }
    assert(noShiftreserves[1] != leftShiftreserves[1]);
}
```

**Beanstalk:** Fixed [here](https://github.com/BeanstalkFarms/Basin/pull/66).

**Cyfrin:** Acknowledged.
