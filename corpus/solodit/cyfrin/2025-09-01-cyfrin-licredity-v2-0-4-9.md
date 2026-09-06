---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Missing governor setter boundaries
vuln_class: []
---

# Missing governor setter boundaries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The governor functions `setMinLiquidityLifespan`, `setMinMargin`, and `setDebtLimit` in the `RiskConfigs` contract do not perform any validation on their input parameters. A privileged user (the `governor`) can set these critical risk parameters to any `uint256` value without any constraints.

**Impact:** While these functions are protected by an `onlyGovernor` modifier, the lack of input validation creates a risk of human error or misconfiguration. For example:
- Setting `_minLiquidityLifespan` to an extremely large value could effectively lock user liquidity positions for an unreasonable amount of time.
- Setting `_minMargin` or `_debtLimit` to an excessively high or low value could inadvertently halt core protocol functionality (like borrowing) or expose the protocol to unintended levels of risk.
A simple typo or mistake in units could lead to significant operational issues.

**Recommended Mitigation:** Introduce sensible sanity checks (i.e., minimum and maximum bounds) for these parameters to act as a safeguard against accidental misconfiguration. This can be done by adding `require` statements to validate the input values.

**Licredity:** Fixed in [PR#68](https://github.com/Licredity/licredity-v1-core/pull/68/files), commit [`ba92282`](https://github.com/Licredity/licredity-v1-core/commit/ba92282cb3d8c9061927f20aed335de60e116423).

`minLiquidityLifespan` is given a cap of 7 days, ensure liquidity can be removed eventually. We opt to keep `minMargin` and `debtLimit` flexible, these are the levers we can pull in exceptional situations, for example to stop new debt from being issued after a sudden and drastic drop in anchor pool liquidity

**Cyfrin:** Verified. `minLiquidityLifespan` has a cap of 7 days.
