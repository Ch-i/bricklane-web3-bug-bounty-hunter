---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-oracle-v2-0-2-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-oracle-v2-0
title: The public Black-Scholes helper does not document its parameter units
vuln_class: []
---

# The public Black-Scholes helper does not document its parameter units

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md)_

---

**Description:** `OracleReceipt::price(uint256,uint256,uint256,uint256,bool)` documents `moneyness`, but not the other parameters. `timeToExpiry` is expressed in seconds, while `moneyness`, `vol_`, and `rate_` are WAD-scaled. A direct caller can silently obtain the wrong result by assuming all numeric arguments use the same scale.

**Recommended Mitigation:** Add NatSpec for every parameter, explicitly stating that `timeToExpiry` is in seconds and that `moneyness`, `vol_`, and `rate_` are WAD-scaled.

**GreekFi:** Fixed in [PR38](https://github.com/greekfi/contracts/pull/38)

**Cyfrin:** Verified. The Black-Scholes helper now documents the units and meaning of every parameter.
