---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-08-21T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0
title: Incorrect state update in `RiskOracle::_processUpdate`
vuln_class: []
---

# Incorrect state update in `RiskOracle::_processUpdate`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** Within the `RiskParameterUpdate` struct, there is a field [`bytes previousValue`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L15) that is intended to store the previous value of a parameter. This state update is performed within [`RiskOracle::_processUpdate`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L156-L158) with the [value obtained](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L155) from the `updatedById` mapping; however, there is no differentiation between parameters for different update types and markets so this state update will be inaccurate with overwhelming likelihood when there are multiple update types/markets. As such, consumers of this contract will receive recommendations with previous values that could be wildly different from what is expected and perhaps execute risk parameter updates based on a delta that is not representative of the real change.

**Impact:** The `previousValue` state for a given update will be incorrect with a very high likelihood and could result in consumers making risk parameter updates based on inaccurate historical data.

**Proof of Concept:** The following test was written to demonstrate this finding and has since been added to the repository during this engagement.

```solidity
function test_PreviousValueIsCorrectForSpecificMarketAndType() public {
    bytes memory market1 = abi.encodePacked("market1");
    bytes memory market2 = abi.encodePacked("market2");
    bytes memory newValue1 = abi.encodePacked("value1");
    bytes memory newValue2 = abi.encodePacked("value2");
    bytes memory newValue3 = abi.encodePacked("value3");
    bytes memory newValue4 = abi.encodePacked("value4");
    string memory updateType = initialUpdateTypes[0];

    vm.startPrank(AUTHORIZED_SENDER);

    // Publish first update for market1 and type1
    riskOracle.publishRiskParameterUpdate(
        "ref1", newValue1, updateType, market1, abi.encodePacked("additionalData1")
    );

    // Publish second update for market1 and type1
    riskOracle.publishRiskParameterUpdate(
        "ref2", newValue2, updateType, market1, abi.encodePacked("additionalData2")
    );

    // Publish first update for market2 and type1
    riskOracle.publishRiskParameterUpdate(
        "ref3", newValue3, updateType, market2, abi.encodePacked("additionalData3")
    );

    // Publish first update for market1 and type1
    riskOracle.publishRiskParameterUpdate(
        "ref4", newValue4, updateType, market1, abi.encodePacked("additionalData4")
    );

    vm.stopPrank();

    // Fetch the latest update for market1 and type1
    RiskOracle.RiskParameterUpdate memory latestUpdateMarket1Type1 =
        riskOracle.getLatestUpdateByParameterAndMarket(updateType, market1);
    assertEq(latestUpdateMarket1Type1.previousValue, newValue2);

    // Fetch the latest update for market2 and type1
    RiskOracle.RiskParameterUpdate memory latestUpdateMarket2Type1 =
        riskOracle.getLatestUpdateByParameterAndMarket(updateType, market2);
    assertEq(latestUpdateMarket2Type1.previousValue, bytes(""));
}
```

**Recommended Mitigation:** Retrieve the correct historical value using the [`latestUpdateIdByMarketAndType`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L28) mapping.

**Chaos Labs:** Fixed in commit [d16a227](https://github.com/ChaosLabsInc/risk-oracle/commit/d16a2277f7fb0efee0053389492aa116543a2bf7).

**Cyfrin:** Verified, the previous update value is now retrieved from the correct identifier.

\clearpage
