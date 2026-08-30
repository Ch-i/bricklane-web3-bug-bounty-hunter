---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Fees never deducted in `AccountableOpenTerm` loan
vuln_class: []
---

# Fees never deducted in `AccountableOpenTerm` loan

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** In `AccountableOpenTerm`, `interestData()` returns non-zero `performanceFee` and `establishmentFee`, but no path ever charges these fees. `_accrueInterest()` only updates `_scaleFactor` for base interest and none of `supply` or `repay` calls `FeeManager` (unlike FixedTerm’s `collect`). As a result, fees are never charged.

**Impact:** Protocol/manager fees are effectively never taken.

**Recommended Mitigation:** Consider charge the fee in `supply()`/`repay()`, before any other state changes. Compute fees for the elapsed period and transfer to `FeeManager`, then proceed.

**Accountable:** Fixed in commits [`fce6961`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/fce6961c71269739ec35da60131eaf63e66e1726) and [`8e53eba`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/8e53eba7340f223f86c9c392f50b8b2d885fdd39)

**Cyfrin:** Verified. `performanceFee` and `establishmentFee` are now deducted for open term loans.
