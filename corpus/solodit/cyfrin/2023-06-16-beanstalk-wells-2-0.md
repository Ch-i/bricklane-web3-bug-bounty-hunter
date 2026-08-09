---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: TWAP is incorrect when only 1 update has occurred
vuln_class: []
---

# TWAP is incorrect when only 1 update has occurred

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

**Description:** If there has only been a single update to the pump, `GeoEmaAndCumSmaPump::readTwaReserves` will return an incorrect value.

**Impact:** Given this affects only one oracle update when the pump is still ramping up, we evaluate the severity to LOW.

**Proof of Concept:**
```solidity
// NOTE: place in `Pump.Update.t.sol`
function testTWAReservesIsWrong() public {
    increaseTime(12); // increase 12 seconds

    bytes memory startCumulativeReserves = pump.readCumulativeReserves(
        address(mWell)
    );
    uint256 lastTimestamp = block.timestamp;
    increaseTime(120); // increase 120 seconds aka 10 blocks

    (uint[] memory twaReserves, ) = pump.readTwaReserves(
        address(mWell),
        startCumulativeReserves,
        lastTimestamp
    );

    assertApproxEqAbs(twaReserves[0], 1e6, 1);
    assertApproxEqAbs(twaReserves[1], 2e6, 1);

    vm.prank(user);
    // gonna double it
    // so our TWAP should now be ~1.5 & 3
    b[0] = 2e6;
    b[1] = 4e6;
    mWell.update(address(pump), b, new bytes(0));

    increaseTime(120); // increase 12 seconds aka 10 blocks
    (twaReserves, ) = pump.readTwaReserves(
        address(mWell),
        startCumulativeReserves,
        lastTimestamp
    );

    // the reserves of b[0]:
    // - 1e6 * 10 blocks
    // - 2e6 * 10 blocks
    // average reserves over 20 blocks:
    // - 15e5
    // assertApproxEqAbs(twaReserves[0], 1.5e5, 1);
    // instead, we get:
    // b[0] = 2070529

    // the reserves of b[1]:
    // - 2e6 * 10 blocks
    // - 4e6 * 10 blocks
    // average reserves over 20 blocks:
    // - 3e6
    assertApproxEqAbs(twaReserves[1], 3e6, 1);
    // instead, we get:
    // b[1] = 4141059
}
```

**Recommended Mitigation:** Disallow reading from the pump with fewer than 2 updates.

**Beanstalk:** This is due to a bug in `MockReserveWell`. Before the Well would make the Pump update call with the new reserves. However, the Well should update the Pump with the previous reserves.

This issue with `MockReserveWell` has been fixed [here](https://github.com/BeanstalkFarms/Basin/commit/6f55fb4835dba6f7b4a69c22687c83039cac2af1#diff-e982575c648d2eaa2de1e69b9ea2f4e91b7ffdeb9455ddacd86c70239972dc84).

Upon running the test now, you will see that `twaReserve[0] = 1414213`. This is expected as `sqrt(1e6 * 2e6) = 1414213`. Also, `twaReserve[1] = 2828427`. This is also expected as `sqrt(2e6 * 4e6) = 2828427`.

**Cyfrin:** Acknowledged.
