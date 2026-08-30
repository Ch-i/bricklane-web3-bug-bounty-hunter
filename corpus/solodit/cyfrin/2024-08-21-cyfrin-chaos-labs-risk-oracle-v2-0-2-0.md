---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-21T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0
title: Unnecessary initialization can be removed
vuln_class: []
---

# Unnecessary initialization can be removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** Initialization of the `updateCounter` state variable [within the constructor](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L64) of `RiskOracle` is unnecessary and can be removed since this state will be `0` by default.

**Chaos Labs:** Fixed in commit [9f7375a](https://github.com/ChaosLabsInc/risk-oracle/commit/9f7375a8291deb04719ec4ddbfff1eb638db55e1).

**Cyfrin:** Verified, the initialization is no longer present.
