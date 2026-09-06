---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-1-2
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
title: Duplicated validation can be moved to shared internal function
vuln_class: []
---

# Duplicated validation can be moved to shared internal function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** Currently, both `RiskOracle::publishRiskParameterUpdate` and `RiskOracle::publishBulkRiskParameterUpdates` contain essentially the same validation:
```solidity
// `RiskOracle::publishRiskParameterUpdate`:
require(validUpdateTypes[updateType], "Unauthorized update type.");

// `RiskOracle::publishBulkRiskParameterUpdates`:
require(validUpdateTypes[updateTypes[i]], "Unauthorized update type at index");
```
Both functions also call the internal `_processUpdate()` function, so this validation can be de-duplicated by placing it there instead.

**Chaos Labs:** Fixed in commit [6cf09fb](https://github.com/ChaosLabsInc/risk-oracle/commit/6cf09fbe31a2050d04b60c79eddfa15f5cd5ca15).

**Cyfrin:** Verified, the validation is now present in the shared internal function.
