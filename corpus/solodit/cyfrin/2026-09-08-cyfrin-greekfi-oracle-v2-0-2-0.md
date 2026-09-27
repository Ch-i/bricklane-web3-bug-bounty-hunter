---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-oracle-v2-0-2-0
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
title: '`OracleReceipt::price` wraps oversized call moneyness into a negative signed
  value'
vuln_class: []
---

# `OracleReceipt::price` wraps oversized call moneyness into a negative signed value

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md)_

---

**Description:** `Factory::createOption2` permits an arbitrarily large nonzero strike when the consideration token has no more decimals than the collateral token. If an integration attaches `OracleReceipt` to such a call market, `OracleReceipt::price` can compute moneyness above `type(int256).max`. The pure pricing boundary then converts that unsigned value to `int256`, wrapping it to a negative number before the logarithm and intrinsic-value calculations.

**Impact:** Pricing a deliberately extreme call market can revert while the market is live and can return zero or revert after the exercise deadline, depending on the wrapped value. This fails closed rather than overvaluing collateral, and the documented Morpho deployment accepts only puts, so the supported production profile is not exposed. Generic integrations that use `OracleReceipt` for call markets can nevertheless receive a broken mark.

**Recommended Mitigation:** Reject moneyness above `type(int256).max` before the cast in `OracleReceipt::price`. An integration that supports only a narrower market profile should also validate the Receipt's flavor and strike range before deploying the oracle.

**GreekFi:** Fixed in [PR38](https://github.com/greekfi/contracts/pull/38)

**Cyfrin:** Verified. OracleReceipt now rejects moneyness values above the signed-integer range before casting them.
