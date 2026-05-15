---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Redundant collateral balance check in `_openLoanMorpho`
vuln_class: []
---

# Redundant collateral balance check in `_openLoanMorpho`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance::_openLoanMorpho` contains a redundant check for collateral balance availability. The function verifies that the flash loan contract has sufficient collateral balance, but this check is already performed in the calling `_openLoanPosition` function.

**Recommended Mitigation:**
```diff
    function _openLoanMorpho(
        Id morphoMarketId,
        uint256 borrowAmount,
        address collateralAddress,
        uint256 collateralBalance,
        address rockoWallet
    ) private {
        _checkAllowanceAndApproveContract(address(MORPHO), collateralAddress, collateralBalance);
        MarketParams memory marketParams = MORPHO.idToMarketParams(morphoMarketId);
-       uint256 flashLoanContractBalance = IERC20(collateralAddress).balanceOf(FLASH_LOAN_CONTRACT);
-       // emit LogBalance("Flash Loan Contract Balance", flashLoanContractBalance);
-       require(
-           flashLoanContractBalance >= collateralBalance,
-           "Insufficient collateral available in the flash contract"
-       );
```

**Rocko:** Fixed in commit [a8efb43](https://github.com/getrocko/onchain/commit/a8efb43b10673508e1fd184aec23a5373f73cd5d).

**Cyfrin:** Verified.

\clearpage
