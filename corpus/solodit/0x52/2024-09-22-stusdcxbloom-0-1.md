---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[H-02] BloomPool#\_normalize price will cause severe mis-pricing for RWAs
  that are not 18 dp'
vuln_class: []
---

# [H-02] BloomPool#\_normalize price will cause severe mis-pricing for RWAs that are not 18 dp

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[BloomPool.sol#L349-L351](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L349-L351)

    uint256 totalValue = (existingCollateral.mulWad(startPrice) + amount.mulWad(currentPrice)) / _rwaScalingFactor;
    uint256 totalCollateral = existingCollateral + amount;
    return uint128(totalValue.divWad(totalCollateral));

When calculating the totalValue, \_rwaScalingFactor is used above even though it is not necessary. Both `currentPrice` and `startPrice` are 18 dp and `amount` and `existingCollateral` are the same precision since the measure the same asset. Without `_rwaScalingFactor` total value shares the same precision as `totalCollateral`. This make any decimal scaling unnecessary.

Assuming we have a RWA that is less than 18 dp, our totalValue will be scaled downward by `18 - rwa dp`. This would propagate through to the final price calculation, resulting in a completely incorrect price.

**Lines of Code**

[BloomPool.sol#L344-L352](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L344-L352)

**Recommendation**

`_rwaScalingFactor` should be completely removed from the `totalValue` calculation

**Remediation**

Fixed as recommended in bloom-v2 [PR#17](https://github.com/Blueberryfi/bloom-v2/pull/17)
