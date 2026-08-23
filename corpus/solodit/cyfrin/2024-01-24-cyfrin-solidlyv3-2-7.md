---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: '`CollateralWithdrawn` and `CollateralDeposited` events should include relevant
  amounts'
vuln_class: []
---

# `CollateralWithdrawn` and `CollateralDeposited` events should include relevant amounts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** In `RewardsDistributor::withdrawCollateral` add the `_amount` parameter when emitting the `CollateralWithdrawn` event. This is required as the amount sent does not have to be the same as the amount deposited.

Consider adding the amount deposited to the `CollateralDeposited` event as well, since the required collateral amount could be changed meaning that the current value may not be true for every collateral deposit that has occurred.

**Solidly:**
Fixed in commit [6481747](https://github.com/SolidlyV3/v3-rewards/commit/6481747737b98c8650a36f87b1aeace815505ba9).

**Cyfrin:**
Verified.

\clearpage
