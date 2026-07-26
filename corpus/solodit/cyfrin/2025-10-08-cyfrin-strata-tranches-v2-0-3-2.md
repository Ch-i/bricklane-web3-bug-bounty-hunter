---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Inconsistent Risk Premium Validation in `Accounting` Allows Future Underflows
  or Zero APR
vuln_class: []
---

# Inconsistent Risk Premium Validation in `Accounting` Allows Future Underflows or Zero APR

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** `Accounting::calculateRiskPremium` computes `risk = riskX + riskY * pow(tvlRatio, riskK)`.
 `Accounting::setRiskParameters` checks that `risk < 1e18` (i.e., less than 100%) immediately after updating the parameters, using the current TVL. However, TVL can change later, so `risk` may become `>= 1e18`. In `Accounting::updateIndexes`, the expression `UD60x18.wrap(1e18) - risk` will yield `0` if `risk == 1e18` (making `aprSrt1` zero) and will revert due to underflow if `risk > 1e18`. This creates an inconsistency between the functions and can produce unintended zeros or reverts at runtime.


**Impact:**
- If `risk > 1e18` after TVL changes, `Accounting::updateIndexes` reverts on underflow, blocking accounting updates, tranche deposits/withdrawals, and NAV calculations.
- If `risk == 1e18`, `aprSrt1` becomes zero, potentially setting senior APR (`aprSrt`) to low values, leading to incorrect NAV splits and no yield for seniors.

**Recommended Mitigation:** In `Accounting::updateIndexes`, cap `risk` or revert explicitly if `risk >= 1e18`.


**Strata:**
Fixed in commit [151661](https://github.com/Strata-Money/contracts-tranches/commit/15166175a98837a26cb2d7fa818504fe21a2e788#diff-a2568622a4f3086b894ddad2f673e1f98ab5cf2f6ab7110ac3bb75fa0331b1f4R376-R379) by calculating risk with the maximum TVLsrt ratio: 1 instead of using the current TVLsrt.

**Cyfrin:** Verified.
