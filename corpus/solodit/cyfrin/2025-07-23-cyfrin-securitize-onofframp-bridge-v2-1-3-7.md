---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Unnecessary complexity in `calculateLiquidityTokenAmountWithoutFee`
vuln_class: []
---

# Unnecessary complexity in `calculateLiquidityTokenAmountWithoutFee`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `SecuritizeOffRamp::calculateLiquidityTokenAmountWithoutFee` function contains unnecessary complexity through its three-branch conditional logic that handles decimal conversions between asset and liquidity tokens.

This redundant branching increases code complexity, gas consumption, and potential for inconsistent rounding behavior between branches. The function can be significantly simplified while maintaining identical functionality.

**Recommended Mitigation:** Since the `rate` parameter is expressed in liquidity decimals, the function can be simplified to a single calculation that handles all decimal scenarios:

```solidity
function calculateLiquidityTokenAmountWithoutFee(
    uint256 assetAmount,
    uint256 rate,
    uint256 liquidityDecimals,
    uint256 assetDecimals
) internal pure returns (uint256) {
    return (assetAmount * rate) / (10 ** assetDecimals);
}
```

**Securitize:** Fixed in [2bb438](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/2bb4384976d1a75a00678c0ea74b403d95efb656) and [0deec2](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/0deec2c111de751fed8dc8b7e7faa06d129ec07c).

**Cyfrin:** Verified.
There was a miscommunication around the decimals of NAV rate and the original recommendation was not accurate.
The team confirmed that the rate is NOT in any other liquidity token decimals but is in the decimal of the asset token itself.
While this is not common practice in other protocols and it introduces some weird computation, the mitigated formula itself is technically correct.
