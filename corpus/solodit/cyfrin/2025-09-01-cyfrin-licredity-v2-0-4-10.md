---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-10
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Confusing timestamp naming in `ChainlinkOracle`
vuln_class: []
---

# Confusing timestamp naming in `ChainlinkOracle`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** In `ChainlinkOracle`, the timestamp variables are named in a confusing way. `currentTimeStamp` actually stores the last update time, and `lastUpdateTimeStamp` stores the previous update time. [`ChainlinkOracle::update`](https://github.com/Licredity/licredity-v1-core/blob/1ec4b09826b4299a572e02accb75e8458385c943/src/ChainlinkOracle.sol#L102-L107) moves `currentTimeStamp → lastUpdateTimeStamp` before setting `currentTimeStamp = block.timestamp`, but the names suggest “current” means “now,” which it does not:
```solidity
// if timestamp has changed, update cache
if (block.timestamp != currentTimeStamp) {
    lastPriceX96 = currentPriceX96;
    lastUpdateTimeStamp = currentTimeStamp;
    currentTimeStamp = block.timestamp;
}
```
Consider renaming for clarity, e.g.:
* `currentTimeStamp` → `lastUpdateTimestamp`
* `lastUpdateTimeStamp` → `prevUpdateTimestamp`”

**Licredity:** Acknowledged. But we are OK as is.
