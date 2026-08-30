---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Zero price validation could be included in the price oracle
vuln_class: []
---

# Zero price validation could be included in the price oracle

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `FeeController.calculateTokenAmount()` validates that the price returned by the oracle is non-zero:

```solidity
    function calculateTokenAmount(address token, uint256 feeInUSD) external view returns (uint256) {
        bytes32 oracleID = oracle.oracleID(token);

        if (oracleID == bytes32(0)) {
            revert NoOracleExist();
        }

        uint256 tokenPrice = oracle.getTokenPrice(token);

@>      if (tokenPrice == 0) {
            revert InvalidTokenWithPriceOfZero();
        }

        return feeInUSD * 10 ** 18 / tokenPrice;
    }
```

Instead, this could be included in `PriceOracle._scalePythPrice()` which already validates the price is non-negative:

```solidity
    function _scalePythPrice(int256 _price, int32 _expo) internal pure returns (uint256) {
@>      if (_price < 0) {
            revert NegativePriceNotAllowed();
        }
        ...
    }
```

**Recommended Mitigation:**
```diff
    function _scalePythPrice(int256 _price, int32 _expo) internal pure returns (uint256) {
--      if (_price < 0) {
++      if (_price <= 0) {
            revert NegativePriceNotAllowed();
        }
        ...
    }

    function calculateTokenAmount(address token, uint256 feeInUSD) external view returns (uint256) {
        ...
--      if (tokenPrice == 0) {
--          revert InvalidTokenWithPriceOfZero();
--      }

        return feeInUSD * 10 ** 18 / tokenPrice;
    }
```

**OctoDeFi:** Fixed in PR [\#18](https://github.com/octodefi/strategy-builder-plugin/pull/18).

**Cyfrin:** Verified. The validation is now performed exclusively within the price oracle.
