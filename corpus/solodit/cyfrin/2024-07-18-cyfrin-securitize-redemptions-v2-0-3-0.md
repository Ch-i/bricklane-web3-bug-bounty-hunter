---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Precision loss in the `SecuritizeSwap.calculateDsTokenAmount()` function.
vuln_class: []
---

# Precision loss in the `SecuritizeSwap.calculateDsTokenAmount()` function.

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** When `stableCoinDecimals` is greater than `dsTokenDecimals`, the calculation is divided into two parts: dividing by `(10 ** (stableCoinDecimals - dsTokenDecimals))` at `L242` and then multiplying by `10 ** stableCoinDecimals` at `L245`. This can result in a loss of precision.

```solidity
        if (stableCoinDecimals <= dsTokenDecimals) {
            adjustedStableCoinAmount = _stableCoinAmount * (10 ** (dsTokenDecimals - stableCoinDecimals));
        } else {
242         adjustedStableCoinAmount = _stableCoinAmount / (10 ** (stableCoinDecimals - dsTokenDecimals));
        }
        // The InternalNavSecuritizeImplementation uses rate expressed with same number of decimals as stableCoin
245     uint256 dsTokenAmount = adjustedStableCoinAmount * 10 ** stableCoinDecimals / currentNavRate;
```

**Impact:** The calculated `dsTokenAmount` is less than it should be, resulting in a loss of funds for users.

**Proof Of Concept:**

In fact, the correct formula is
```solidity
        dsTokenAmount = _stableCoinAmount * 10 ** dsTokenDecimals / currentNavRate;
```

Let's consider the following scenario:
1. `stableCoinDecimals = 18`
2. `dsTokenDecimals = 6`
3. `currentNavRate = 1e12`(implying `stableCoin : dsToken = 1e6 : 1`)
4. `_stableCoinAmount = 1e18 - 1`

The current logic calculates as follows:
- `L242`: `adjustedStableCoinAmount = (1e18 - 1) / (10 ** (18 - 6)) = 1e6 - 1`
- `L245`: `dsTokenAmount = (1e6 - 1) * 10 ** 18 / 1e12 = 1e12 - 1e6`

However, the actual correct `dsTokenAmount` should be `(1e18 - 1) * 1e6 / 1e12 = 1e12 - 1`, resulting in a difference of `1e6 - 1`.

**Recommended Mitigation:** The intermediate variable `adjustedStableCoinAmount` is unnecessary.

```diff
    function calculateDsTokenAmount(uint256 _stableCoinAmount) internal view returns (uint256, uint256) {
        uint256 stableCoinDecimals = ERC20(address(stableCoinToken)).decimals();
        uint256 dsTokenDecimals = ERC20(address(dsToken)).decimals();
        uint256 currentNavRate = navProvider.rate();

-       uint256 adjustedStableCoinAmount;
-       if (stableCoinDecimals <= dsTokenDecimals) {
-           adjustedStableCoinAmount = _stableCoinAmount * (10 ** (dsTokenDecimals - stableCoinDecimals));
-       } else {
-           adjustedStableCoinAmount = _stableCoinAmount / (10 ** (stableCoinDecimals - dsTokenDecimals));
-       }
-       // The InternalNavSecuritizeImplementation uses rate expressed with same number of decimals as stableCoin
-       uint256 dsTokenAmount = adjustedStableCoinAmount * 10 ** stableCoinDecimals / currentNavRate;

+       uint256 dsTokenAmount = _stableCoinAmount * 10 ** dsTokenDecimals / currentNavRate;

        return (dsTokenAmount, currentNavRate);
    }
```


**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28)

**Cyfrin:** Verified.
