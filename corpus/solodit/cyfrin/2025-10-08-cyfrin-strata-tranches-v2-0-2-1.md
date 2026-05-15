---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Reducing reserves requesting `USDe` as the asset to receive causes the Strategy
  to release more `sUSDe` than necessary
vuln_class: []
---

# Reducing reserves requesting `USDe` as the asset to receive causes the Strategy to release more `sUSDe` than necessary

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** When reducing reserves and asking for `USDe`, the Strategy incorrectly transfers sUSDe for the actual amount of asked `USDe` (`tokenAmount`) instead of only transferring the required `sUSDe` to cover the requested `tokenAmount` of `USDe`.

```solidity
//sUSDeStrategy::reduceReserve()//
    function reduceReserve (address token, uint256 tokenAmount, address receiver) external onlyCDO {
        ...
        if (token == address(USDe)) {
            //@audit-issue => transfer sUSDe for `tokenAmount` which is in USDe.
            unstakeCooldown.transfer(sUSDe, receiver, tokenAmount);
            return;
        }
        revert UnsupportedToken(token);
    }
```

**Impact:** The strategy releases more sUSDe than necessary to cover the USDe requested to be withdrawn when reducing reserves and asking USDe. This means that depositors end up incurring a loss because the strategy is left with less USDe than it should have.

**Proof of Concept:** For example, if the `sUSDe` <=> `USDe` rate is 1:1.5, and it is requested to reduce reserves for 150 USDe.
- The Strategy will send 150 `sUSDe` (which are worth `225 USDe`) to the `treasury` **instead of only sending** `100 sUSDe` (worth `150 USDe`).


**Recommended Mitigation:** When reducing reserves asking for USDe, on `sUSDeStrategy::reduceReserve`, call `sUSDe::previewWithdraw` to get how much sUSDe is required to obtain the requested `tokenAmount` of `USDe`, and transfer that amount of `sUSDe` to the `UnstakeCooldown` contract.
```solidity
    function reduceReserve (address token, uint256 tokenAmount, address receiver) external onlyCDO {
       ...
        if (token == address(USDe)) {
+           uint256 shares = sUSDe.previewWithdraw(tokenAmount);
+           unstakeCooldown.transfer(sUSDe, receiver, shares);
-           unstakeCooldown.transfer(sUSDe, receiver, tokenAmount);
            return;
        }
        revert UnsupportedToken(token);
    }
```

**Strata:**
Fixed in commit [953c3bc](https://github.com/Strata-Money/contracts-tranches/commit/953c3bc8ee4b5aaca955eabb07ab1c5e62c28166) by converting `tokenAmount` to `shares` in `sUSDe` units.

**Cyfrin:** Verified.
