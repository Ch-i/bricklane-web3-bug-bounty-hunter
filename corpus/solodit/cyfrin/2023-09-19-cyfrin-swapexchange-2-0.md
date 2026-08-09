---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-swapexchange-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-swapexchange
title: Not proper variable naming
vuln_class: []
---

# Not proper variable naming

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-swapexchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md)_

---

**Severity:** Informational

**Description:** The contract `FeeData` has a internal variable `_feeValue` that is used to calculate the fee.
Across the usage of this variable, it is used as a numerator while calculating the fee percentage.
We recommend renaming this variable to `feeNumerator` to avoid confusion.

```solidity
FeeUtils.sol
16:     function _calculateFees(uint256 amountA, uint256 amountB, uint8 feeType,  uint256 hops, uint256 feeValue, uint256 feeDenominator, uint256 fixedFee)
17:     internal pure returns (uint256) {
18:         if (feeType == Constants.FEE_TYPE_TOKEN_B) {
19:             return MathUtils._mulDiv(amountB, feeValue, feeDenominator) * hops;
20:         }
21:         if (feeType == Constants.FEE_TYPE_TOKEN_A) {
22:             return MathUtils._mulDiv(amountA, feeValue, feeDenominator) * hops;
23:         }
24:         if (feeType == Constants.FEE_TYPE_ETH_FIXED) {
25:             return fixedFee * hops;
26:         }
27:         revert Errors.UnknownFeeType(feeType);
28:     }
```

**Protocol:** Fixed in commit [f6154c9](https://github.com/SwapExchangeio/Contracts/commit/f6154c99edabe7b62d956935a94567c88ee89b3d).

**Cyfrin:** Verified.
