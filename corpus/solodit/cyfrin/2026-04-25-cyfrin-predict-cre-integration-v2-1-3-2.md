---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Cache `roundConfigIndices[feedId][interval]` inside `_createRound` loops
vuln_class: []
---

# Cache `roundConfigIndices[feedId][interval]` inside `_createRound` loops

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `ChainlinkUpDownAdapter::_createRound` is called inside `extend` and `_initialize` loops (up to `roundCount` iterations). Each call reads `roundConfigIndices[feedId][interval]` via `_getRound` / `roundKey`. The index never changes within the loop; caching once outside avoids N-1 redundant warm SLOADs (~100 gas each).

```solidity
ChainlinkUpDownAdapter.sol
103:        for (uint32 i = 1; i <= roundCount; i++) {
104:            ts += interval;
105:            _createRound(feedId, ts, interval);
106:        }
302:    function _createRound(bytes32 feedId, uint32 startTimestamp, uint32 interval) private {
305:        rounds[roundKey(feedId, interval, roundConfigIndices[feedId][interval], startTimestamp)] = questionID;
```

**Impact:** ~100 gas per extra loop iteration wasted on redundant warm SLOADs.

**Recommended Mitigation:**
```solidity
uint256 idx = roundConfigIndices[feedId][interval];
for (uint32 i; i < roundCount; i++) {
    bytes32 questionID = keccak256(abi.encode(feedId, interval, ts));
    CTF.prepareCondition(questionID, 2);
    rounds[roundKey(feedId, interval, idx, ts)] = questionID;
    emit ChainlinkUpDownAdapter__RoundCreated(feedId, interval, ts, questionID);
    ts += interval;
}
```

**Predict.fun:** Acknowledged; we prefer the current version for readability.
