---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-0-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`SecuritizeOnRamp::swap` and `SecuritizeOffRamp::redeem` pass operator as
  investor address resulting in denial of service'
vuln_class: []
---

# `SecuritizeOnRamp::swap` and `SecuritizeOffRamp::redeem` pass operator as investor address resulting in denial of service

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeOnRamp::swap` and `SecuritizeOffRamp::redeem` have modifier `onlyRole(OPERATOR_ROLE)` meaning only an operator can call these functions.

But when calling child functions such as `BaseOnRamp::_swap` or `BaseOffRamp::_redeem`, they pass `_msgSender()` as the investor wallet which is incorrect since the operator and the investor are not the same entities.

**Impact:** The most likely impact is temporary denial of service; these functions will revert as the operator is not also an investor. But the contracts are upgradeable so can be fixed or in a worst-case scenario re-deployed.

**Recommended Mitigation:** If these functions are designed to be called by investors then remove the modifier `onlyRole(OPERATOR_ROLE)`.

Otherwise if they are supposed to be called by an operator, then add an input parameter to specify the investor address.

Also see the related issue M-1 "Incorrect use of `investorExists` modifier in `PublicStockOnRamp::swap`" which may also be relevant here.

**Securitize:** Fixed in commit [5cbd6d8](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/5cbd6d82e9bff57c6441334897e8ef0c9c594825) by removing the `onlyRole` as these functions are intended to be directly called by investors.

**Cyfrin:** Verified.

\clearpage
