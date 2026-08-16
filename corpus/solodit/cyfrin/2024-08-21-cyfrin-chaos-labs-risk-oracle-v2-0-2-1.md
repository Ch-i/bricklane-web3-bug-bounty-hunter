---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-08-21T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0
title: Array length validation is not necessary
vuln_class: []
---

# Array length validation is not necessary

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** [`RiskOracle::publishBulkRiskParameterUpdates`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L117-L142) currently validates that the lengths of all input arrays are equal.

```solidity
function publishBulkRiskParameterUpdates(
    string[] memory referenceIds,
    bytes[] memory newValues,
    string[] memory updateTypes,
    bytes[] memory markets,
    bytes[] memory additionalData
) external onlyAuthorized {
    require(
        referenceIds.length == newValues.length && newValues.length == updateTypes.length
            && updateTypes.length == markets.length && markets.length == additionalData.length,
        "Mismatch between argument array lengths."
    );
    for (uint256 i = 0; i < referenceIds.length; i++) {
        require(validUpdateTypes[updateTypes[i]], "Unauthorized update type at index");
        _processUpdate(referenceIds[i], newValues[i], updateTypes[i], markets[i], additionalData[i]);
    }
}
```

This validation can be removed on account of the loop over `referenceIds`, as a length mismatch will either revert due to out-of-bounds access or result in additional elements beyond the length of the `referenceIds` array being ignored.

**Chaos Labs:** Fixed in commit [6cf09fb](https://github.com/ChaosLabsInc/risk-oracle/commit/6cf09fbe31a2050d04b60c79eddfa15f5cd5ca15).

**Cyfrin:** Verified, the validation has been removed.

\clearpage
