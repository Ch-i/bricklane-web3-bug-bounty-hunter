---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: '`rETH` staleness configuration does not match documentation'
vuln_class: []
---

# `rETH` staleness configuration does not match documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** `ORACLE_CONFIG.md` states that all feeds use a 25-hour staleness threshold, but deployment code configures rETH differently.

- Doc claim: ORACLE_CONFIG.md:30
- Actual deployment value: `RETH_ETH_STALENESS_THRESHOLD = 48 hours` at DeployLiquity2.s.sol:119
- That 48h value is passed to `RETHPriceFeed` at DeployLiquity2.s.sol:892

This is a documentation/config inconsistency.

**Impact:** Operational and audit assumptions can be wrong. Parties relying on docs may expect rETH oracle stale-data handling at 25h, while deployed behavior tolerates up to 48h for the `RETH-ETH` leg. This can affect incident response expectations and risk modeling for oracle freshness.


**Recommended Mitigation:** Align docs and code to a single source of truth.

**Firm Money:**
Fixed in [PR13](https://github.com/firm-money/firm/pull/13).

**Cyfrin:** Verified.
