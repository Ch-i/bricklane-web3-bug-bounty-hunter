---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Multiplication could overflow in `RebasingLibrary` for tokens with greater
  than 18 decimals
vuln_class: []
---

# Multiplication could overflow in `RebasingLibrary` for tokens with greater than 18 decimals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `RebasingLibrary` contains special handling for tokens with greater than 18 decimals:
```solidity
// convertTokensToShares
        } else {
            uint256 scale = 10**(_tokenDecimals - 18);
            return (_tokens * DECIMALS_FACTOR + (_rebasingMultiplier * scale) / 2) / (_rebasingMultiplier * scale);
        }

// convertSharesToTokens
        } else {
            uint256 scale = 10**(_tokenDecimals - 18);
            return (_shares * _rebasingMultiplier * scale + DECIMALS_FACTOR / 2) / DECIMALS_FACTOR;
        }
```

**Impact:** When using tokens with high decimal values, the multiplication here could overflow causing denial of service.

**Recommended Mitigation:** Use OpenZeppelin's [Math::mulDiv](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol#L204), fixed code also incorporates suggested fix for L-1:
```solidity
pragma solidity 0.8.22;

import {Math} from "@openzeppelin/contracts/utils/math/Math.sol";

library RebasingLibrary {
    uint256 private constant DECIMALS_FACTOR = 1e18;

    function convertTokensToShares(
        uint256 _tokens,
        uint256 _rebasingMultiplier,
        uint8 _tokenDecimals
    ) internal pure returns (uint256 shares) {
        require(_rebasingMultiplier > 0, "Invalid rebasing multiplier");

        if (_tokenDecimals == 18) {
            return Math.mulDiv(_tokens, DECIMALS_FACTOR, _rebasingMultiplier);
        } else if (_tokenDecimals < 18) {
            uint256 scale = 10**(18 - _tokenDecimals);
            // tokens * scale * DECIMALS_FACTOR / multiplier
            return Math.mulDiv(_tokens * scale, DECIMALS_FACTOR, _rebasingMultiplier);
        } else {
            uint256 scale = 10**(_tokenDecimals - 18);
            // tokens * DECIMALS_FACTOR / (multiplier * scale)
            return Math.mulDiv(_tokens, DECIMALS_FACTOR, _rebasingMultiplier * scale);
        }
    }

    function convertSharesToTokens(
        uint256 _shares,
        uint256 _rebasingMultiplier,
        uint8 _tokenDecimals
    ) internal pure returns (uint256 tokens) {
        require(_rebasingMultiplier > 0, "Invalid rebasing multiplier");

        if (_tokenDecimals == 18) {
            return Math.mulDiv(_shares, _rebasingMultiplier, DECIMALS_FACTOR);
        } else if (_tokenDecimals < 18) {
            uint256 scale = 10**(18 - _tokenDecimals);
            // (shares * multiplier / DECIMALS_FACTOR) / scale
            return Math.mulDiv(_shares, _rebasingMultiplier, DECIMALS_FACTOR * scale);
        } else {
            uint256 scale = 10**(_tokenDecimals - 18);
            // shares * multiplier * scale / DECIMALS_FACTOR
            return Math.mulDiv(_shares * scale, _rebasingMultiplier, DECIMALS_FACTOR);
        }
    }
}
```

**Securitize:** Fixed in commit [9b81e76](https://github.com/securitize-io/dstoken/commit/9b81e76c6d75f8e550f719a27c344cb337377d79) by reverting for tokens with greater than 18 decimals.

**Cyfrin:** Verified.
