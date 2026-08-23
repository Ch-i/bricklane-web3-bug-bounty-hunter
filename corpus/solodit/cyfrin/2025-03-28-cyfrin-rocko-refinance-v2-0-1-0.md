---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Error messages hardcode `USDC` but other debt tokens may be used
vuln_class: []
---

# Error messages hardcode `USDC` but other debt tokens may be used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Error messages hardcode `USDC` but other token may be used, eg:
```solidity
function _closeLoanPositionAndReturnCollateralBalance(
    // @audit debt token can be other tokens apart from USDC but error
    // message hardcodes USDC
    require(
        debtBalance <= IERC20(debtTokenAddress).balanceOf(FLASH_LOAN_CONTRACT),
        "Insufficient USDC available in the flash contract"
    );
```

This code in `onMorphoFlashLoan` also assumes the debt token will be USDC:
```solidity
uint256 usdcBalance = IERC20(ctx.debtTokenAddress).balanceOf(FLASH_LOAN_CONTRACT);
bool feeAmountAvailable = usdcBalance >= feeAmount;
```

**Rocko:** Fixed in commit [ec9f5be](https://github.com/getrocko/onchain/commit/ec9f5be20f9249cd20fcc1e173192361ecd97ef5).

**Cyfrin:** Verified.
