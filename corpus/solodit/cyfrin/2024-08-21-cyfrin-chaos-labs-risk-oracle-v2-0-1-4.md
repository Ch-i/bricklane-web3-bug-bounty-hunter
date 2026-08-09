---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-08-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0
title: Unreachable code can be removed
vuln_class: []
---

# Unreachable code can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** Within [`RiskOracle::_processUpdate`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L155), the `else` branch of the ternary operator is unreachable due to `updateCounter` being initialized to 0 and incremented before this line:

```solidity
updateCounter++;
bytes memory previousValue = updateCounter > 0 ? updatesById[updateCounter - 1].newValue : bytes("");
```

Thus, this variable assignment logic can be simplified to just reading from the mapping (but note that this usage of the `updatedById` mapping is incorrect, as reported in M-01).

**Chaos Labs:** Fixed in commit [6cf09fb](https://github.com/ChaosLabsInc/risk-oracle/commit/6cf09fbe31a2050d04b60c79eddfa15f5cd5ca15).

**Cyfrin:** Verified, the code path has been removed.

\clearpage
