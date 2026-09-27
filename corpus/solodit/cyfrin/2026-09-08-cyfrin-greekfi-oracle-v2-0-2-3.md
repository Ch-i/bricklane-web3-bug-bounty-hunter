---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-oracle-v2-0-2-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-oracle-v2-0
title: '`OracleReceipt::price` can publish zero at its moneyness precision boundary'
vuln_class: []
---

# `OracleReceipt::price` can publish zero at its moneyness precision boundary

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md)_

---

**Description:** `OracleReceipt::price` computes `m = strike * 1e18 / spot` and then returns `(1e18 - optionPrice) * 1e18`. At extreme moneyness, the WAD calculation can floor the Receipt value to zero. In particular, once `timeToExpiry == 0`, a call with `m == 0` returns full intrinsic option value and the outer function publishes a zero Morpho price; before that boundary, `lnWad(0)` reverts instead.

Morpho treats a zero collateral price as zero borrowing capacity and permits collateral-denominated liquidation to compute zero repayment. However, outside the separately reported post-deadline valuation issue, this requires the modelled Receipt value to be below WAD resolution and is not credible for the intended WETH/sUSDe deployment profile. This is precision and fail-closed hardening, not a Low-severity loss scenario.

**Recommended Mitigation:** Handle the boundary explicitly: either calculate moneyness with enough precision to preserve a positive Receipt value or revert when the computation would publish zero. The post-deadline case should continue to be addressed by the separate lifecycle fix.

**GreekFi:** Fixed in [PR38](https://github.com/greekfi/contracts/pull/38)

**Cyfrin:** Verified. OracleReceipt now reverts instead of publishing a zero collateral price.

\clearpage
