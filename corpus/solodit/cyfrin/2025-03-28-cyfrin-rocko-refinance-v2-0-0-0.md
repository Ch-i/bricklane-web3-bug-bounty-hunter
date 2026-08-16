---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Protocol fee should round up in favor of the protocol
vuln_class: []
---

# Protocol fee should round up in favor of the protocol

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Protocol fee should round up in favor of the protocol in `onMorphoFlashLoan`:
```solidity
uint256 rockoFeeBP = ROCKO_FEE_BP;
if (rockoFeeBP > 0) {
    unchecked {
        feeAmount = (flashBorrowAmount * rockoFeeBP) / BASIS_POINTS_DIVISOR;
        borrowAmountWithFee += feeAmount;
    }
}
```

Consider [using](https://x.com/DevDacian/status/1892529633104396479) OpenZeppelin [`Math::mulDiv`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/fda6b85f2c65d146b86d513a604554d15abd6679/contracts/utils/math/Math.sol#L280) with the rounding parameter or Solady [`FixedPointMathLib::fullMulDivUp`](https://github.com/Vectorized/solady/blob/c9e079c0ca836dcc52777a1fa7227ef28e3537b3/src/utils/FixedPointMathLib.sol#L548).

Another benefit of using these libraries is that intermediate overflow from the multiplication of `flashBorrowAmount * rockoFeeBP` is avoided.

**Rocko:** Fixed in commit [a59ba0e](https://github.com/getrocko/onchain/commit/a59ba0e7958c544ad95788ce29923a342a2ea35a).

**Cyfrin:** Verified.
