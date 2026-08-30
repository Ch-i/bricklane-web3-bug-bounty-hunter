---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: '`Accounting::setMinimumJrtSrtRatio` sets `reserveBps` instead of `minimumJrtSrtRatio`
  making ratio configuration impossible'
vuln_class: []
---

# `Accounting::setMinimumJrtSrtRatio` sets `reserveBps` instead of `minimumJrtSrtRatio` making ratio configuration impossible

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The `Accounting::setMinimumJrtSrtRatio` function contains a an implementation error where it modifies the wrong state variable. Instead of setting `minimumJrtSrtRatio`, the function incorrectly sets `reserveBps`, making it impossible to configure the minimum Junior-to-Senior tranche ratio.

```solidity
    function setMinimumJrtSrtRatio (uint256 bps) external onlyOwner {
        require(bps <= RESERVE_BPS_MAX, "ReserveBpsMax");
        reserveBps = bps;
        emit ReservePercentageChanged(reserveBps);
    }
```

**Impact:** Impossible Risk Parameter Configuration: The `minimumJrtSrtRatio` variable can only be set during initialization (currently hardcoded to 5%) and cannot be updated afterward, preventing proper risk management adjustments.

Accidental Reserve Configuration: Calling `setMinimumJrtSrtRatio` thinking it will adjust tranche ratios will instead modify the reserve percentage, leading to unintended reserve allocation changes.

**Recommended Mitigation:** Perform the following changes inside the `Accounting` contract:

```diff

++event MinimumJrtSrtRatioChanged(uint256 minimumJrtSrtRatio);

function setMinimumJrtSrtRatio (uint256 bps) external onlyOwner {
-   require(bps <= RESERVE_BPS_MAX, "ReserveBpsMax");
-   reserveBps = bps;
-   emit ReservePercentageChanged(reserveBps);
+   require(bps <= 1e18, "InvalidRatio"); // Max 100%
+   minimumJrtSrtRatio = bps;
+   emit MinimumJrtSrtRatioChanged(minimumJrtSrtRatio);
}
```
**Strata:**
Fixed in commit [657bde](https://github.com/Strata-Money/contracts-tranches/commit/657bdef3fbb1caa0e90c1d28455523c3f5c94bbf) by updating the correct variable `minimumJrtSrtRatio`.

**Cyfrin:** Verfified.
