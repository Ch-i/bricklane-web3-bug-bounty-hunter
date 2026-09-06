---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`ChainlinkUtil::getPrice` doesn''t check for stale price'
vuln_class: []
---

# `ChainlinkUtil::getPrice` doesn't check for stale price

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** [`ChainlinkUtil::getPrice`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/external/chainlink/ChainlinkUtil.sol#L32-L33) doesn't [check for stale prices](https://medium.com/zaros-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#99af).

**Impact:** Code will execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for users.

**Recommended Mitigation:** Check `updatedAt` returned by `latestRoundData` against each price feed's [individual heartbeat](https://medium.com/zaros-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#fb78). Heartbeats could be stored in:
* `MarginCollateralConfiguration::Data`
* `MarketConfiguration::Data`

**Zaros:** Fixed in commit [c70c9b9](https://github.com/zaros-labs/zaros-core/commit/c70c9b9399af8eb5e351f9b4f43feed82e19ef5b#diff-dc206ca4ca1f5e661061478ee4bd43c0c979d77a1ce1e0f30745d766bcd65394R39-R43).

**Cyfrin:** Verified.
