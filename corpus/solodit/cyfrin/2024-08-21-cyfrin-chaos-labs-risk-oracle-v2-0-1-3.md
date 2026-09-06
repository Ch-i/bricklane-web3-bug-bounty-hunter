---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0
title: Parallel data structures are not necessary
vuln_class: []
---

# Parallel data structures are not necessary

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** Usage of the [`updatesById`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L25) mapping with keys given by the monotonically increasing [`updateCounter`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L29) state variable is effectively the same as using the [`updateHistory`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L25) array with an index shift of 1 (due to 0 being reserved for invalid update ids). In the current design, it is not necessary to maintain these parallel data structures, so if the format of update ids is unlikely to change in the future then this `updatesById` mapping can be removed in favor of the `updateHistory` array. Note that this modification would necessitate additional refactoring in the `getLatestUpdateByType()`, `getLatestUpdateByParameterAndMarket()`, and `getUpdateById()` functions.

**Chaos Labs:** Fixed in commit [6cf09fb](https://github.com/ChaosLabsInc/risk-oracle/commit/6cf09fbe31a2050d04b60c79eddfa15f5cd5ca15).

**Cyfrin:** Verified, the `RiskParameterUpdate[] updateHistory` has been removed.
