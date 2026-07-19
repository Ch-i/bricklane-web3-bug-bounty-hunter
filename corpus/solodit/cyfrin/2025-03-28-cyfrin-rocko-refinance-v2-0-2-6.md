---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Remove redundant `onBehalfOf` variables
vuln_class: []
---

# Remove redundant `onBehalfOf` variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Remove redundant `onBehalfOf` variables:
```diff
    function _supplyToAave(address collateralAddress, uint256 collateralBalance, address rockoWallet) private {
-       address onBehalfOf = rockoWallet;
-       AAVE.supply(collateralAddress, collateralBalance, onBehalfOf, AAVE_REFERRAL_CODE);
+       AAVE.supply(collateralAddress, collateralBalance, rockoWallet, AAVE_REFERRAL_CODE);
    }
    function _borrowFromAave(address rockoWallet, address token, uint256 borrowAmount) private {
-       address onBehalfOf = rockoWallet;
-       AAVE.borrow(token, borrowAmount, AAVE_INTERESTE_RATE_MODE, AAVE_REFERRAL_CODE, onBehalfOf);
+       AAVE.borrow(token, borrowAmount, AAVE_INTERESTE_RATE_MODE, AAVE_REFERRAL_CODE, rockoWallet);
    }
```

**Rocko:** Fixed in commit [751e906](https://github.com/getrocko/onchain/commit/751e906b7c2df6cb587e709b12de25593eb02c75).

**Cyfrin:** Verified.
