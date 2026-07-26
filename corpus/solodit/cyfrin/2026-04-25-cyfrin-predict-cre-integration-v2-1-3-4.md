---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-3-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: 'Fail-fast: move cheap input checks before storage reads'
vuln_class: []
---

# Fail-fast: move cheap input checks before storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Several functions in `ChainlinkUpDownAdapter` perform storage reads before cheap calldata validations. Moving cheap checks first avoids SLOADs on the revert path.

```solidity
ChainlinkUpDownAdapter.sol
85:    function extend(bytes32 feedId, uint32 interval, uint256 roundCount) external onlyRole(EXTENDER_ROLE) {
86:        _validateInterval(interval);   // SLOAD isIntervalValid
87:
88:        if (roundCount == 0) {         // cheap calldata check
89:            revert ChainlinkUpDownAdapter__RoundCountTooLow();
90:        }
```

Saves ~2,100 gas on the `roundCount == 0` revert path. Similarly `initialize` delegates cheap checks (`startTimestamp >= block.timestamp`, `roundCount < 2`, `startPrice == 0`, alignment) after two SLOADs — reordering saves ~2,200 gas on revert.

**Impact:** Wasted SLOAD gas on revert paths.

**Recommended Mitigation:**
```solidity
function extend(bytes32 feedId, uint32 interval, uint256 roundCount) external onlyRole(EXTENDER_ROLE) {
    if (roundCount == 0) revert ChainlinkUpDownAdapter__RoundCountTooLow();
    _validateInterval(interval);
    // ...
}
```

**Predict.fun:** Fixed in commit [b6127d0](https://github.com/PredictDotFun/prediction-market/commit/b6127d08b54d9a58728dc626b28776edd8fc3f54).

**Cyfrin:** Verified.
