---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Both reserves should be checked in `LibWell::getWellPriceFromTwaReserves`
vuln_class: []
---

# Both reserves should be checked in `LibWell::getWellPriceFromTwaReserves`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

**Description:**
```solidity
function getWellPriceFromTwaReserves(address well) internal view returns (uint256 price) {
    AppStorage storage s = LibAppStorage.diamondStorage();
    // s.twaReserve[well] should be set prior to this function being called.
    // 'price' is in terms of reserve0:reserve1.
    if (s.twaReserves[well].reserve0 == 0) {
        price = 0;
    } else {
        price = s.twaReserves[well].reserve0.mul(1e18).div(s.twaReserves[well].reserve1);
    }
}
```

Currently, `LibWell::getWellPriceFromTwaReserves` sets the price to zero if the time-weighted average reserves of the zeroth reserve (for Wells, Bean) is zero. Given the implementation of `LibWell::setTwaReservesForWell`, and that a Pump failure will return an empty reserves array, it does not appear possible to encounter the case where one reserve can be zero without the other except for perhaps an exploit or migration scenario. Therefore, whilst unlikely, it is best to but best to ensure both reserves are non-zero to avoid a potential division by zero `reserve1` when calculating the price as a revert here would result in DoS of `SeasonFacet::gm`.

```solidity
function setTwaReservesForWell(address well, uint256[] memory twaReserves) internal {
    AppStorage storage s = LibAppStorage.diamondStorage();
    // if the length of twaReserves is 0, then return 0.
    // the length of twaReserves should never be 1, but
    // is added for safety.
    if (twaReserves.length < 1) {
        delete s.twaReserves[well].reserve0;
        delete s.twaReserves[well].reserve1;
    } else {
        // safeCast not needed as the reserves are uint128 in the wells.
        s.twaReserves[well].reserve0 = uint128(twaReserves[0]);
        s.twaReserves[well].reserve1 = uint128(twaReserves[1]);
    }
}
```

Additionally, to correctly implement the check identified by the comment in `LibWell::setTwaReservesForWell`, the time-weighted average reserves in storage should be reset if the array length is less-than or equal-to 1.

**Recommended Mitigation:**
```diff
// LibWell::getWellPriceFromTwaReserves`
- if (s.twaReserves[well].reserve0 == 0) {
+ if (s.twaReserves[well].reserve0 == 0 || s.twaReserves[well].reserve1 == 0) {
        price = 0;
} else {

// LibWell::setTwaReservesForWell
- if (twaReserves.length < 1) {
+ if (twaReserves.length <= 1) {
    delete s.twaReserves[well].reserve0;
    delete s.twaReserves[well].reserve1;
} else {
```
