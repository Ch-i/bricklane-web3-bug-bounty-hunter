---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`ChainlinkUpDownAdapter::enableRoundConfig` reads `roundConfigIndices[feedId][interval]`
  twice'
vuln_class: []
---

# `ChainlinkUpDownAdapter::enableRoundConfig` reads `roundConfigIndices[feedId][interval]` twice

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** In `ChainlinkUpDownAdapter::enableRoundConfig`, the current index is read implicitly via `_getCurrentRoundConfig` (line 162) then explicitly again at line 180 (`roundConfigIndices[feedId][interval] + 1`). Both reads are on the success path.

```solidity
ChainlinkUpDownAdapter.sol
162:        RoundConfig storage roundConfig = _getCurrentRoundConfig(feedId, interval);
180:        uint256 newRoundConfigIndex = roundConfigIndices[feedId][interval] + 1;
181:        roundConfigIndices[feedId][interval] = newRoundConfigIndex;
```

**Impact:** Duplicate warm SLOAD (~100 gas) on the success path.

**Recommended Mitigation:**
```solidity
uint256 currentIndex = roundConfigIndices[feedId][interval];
RoundConfig storage roundConfig = roundConfigs[roundConfigKey(feedId, interval, currentIndex)];
// ...
uint256 newRoundConfigIndex = currentIndex + 1;
roundConfigIndices[feedId][interval] = newRoundConfigIndex;
```

**Predict.fun:** Acknowledged; we prefer the current version for readability.
