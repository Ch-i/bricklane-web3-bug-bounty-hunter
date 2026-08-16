---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-03-27-blueberry-staking-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-03-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md
tags:
- firm:0x52
- report:2024-03-27-blueberry-staking
title: '[H-01] Precision error in \_fetchTWAP causes vesting to be free after initial
  lockdrop period'
vuln_class: []
---

# [H-01] Precision error in \_fetchTWAP causes vesting to be free after initial lockdrop period

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2024-03-27-Blueberry-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md)_

---

**Details**

[BlueberryStaking.sol#L830-L843](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L830-L843)

    // Adjust for decimals
    if (BLB_DECIMALS > _decimalsStable) {
        _priceX96 /= 10 ** (BLB_DECIMALS - _decimalsStable);
    } else if (_decimalsStable > BLB_DECIMALS) {
        _priceX96 *= 10 ** (_decimalsStable - BLB_DECIMALS);
    }

    // Now priceX96 is the price of blb in terms of stableAsset, multiplied by 2^96.
    // To convert this to a human-readable format, you can divide by 2^96:

    uint256 _price = _priceX96 / 2 ** 96;

    // Now 'price' is the price of blb in terms of stableAsset, in the correct decimal places.
    return _price;

TWAP prices from Uniswap V3 oracles return in a 64x96 format. Due to its unusual format these values are notoriously hard to manipulate. Directly above the price is converted from base 2 to base 10. The issue is that this conversion gives a final price with 0 dp. \_fetchTWAP is expected to return the price of blb with 18 dp. This large disparity between the expected and actual precision causes it to be essentially free to vest all tokens immediately.

**Lines of Code**

[BlueberryStaking.sol#L798-L844](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L798-L844)

**Recommendation**

Convert to 18 dp with the following lines:

    if (blbIsToken0) {
        return FullMath.mulDiv(_priceX96, 10 ** (18 + BLB_DECIMALS stableDecimals), 2 ** 96);
    } else {
        uint256 inversePrice = FullMath.mulDiv(_priceX96, 10 ** (18 - BLB_DECIMALS + stableDecimals), 2 ** 96);
        return 10**36 / inversePrice;
    }

**Remediation**

Fixed in [PR#30](https://github.com/Blueberryfi/blueberry-staking/pull/30/). Math has been rebuilt, ensuring proper precision is maintained during conversion.
