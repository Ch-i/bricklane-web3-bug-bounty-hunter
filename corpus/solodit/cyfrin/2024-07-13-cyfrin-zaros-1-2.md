---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`ChainlinkUtil::getPrice` will use incorrect price when underlying aggregator
  reaches `minAnswer`'
vuln_class: []
---

# `ChainlinkUtil::getPrice` will use incorrect price when underlying aggregator reaches `minAnswer`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Chainlink price feeds have in-built minimum & maximum prices they will return; if due to an unexpected event an asset’s value falls below the price feed’s minimum price, [the oracle price feed will continue to report the (now incorrect) minimum price](https://medium.com/zaros-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#00ac).

[`ChainlinkUtil::getPrice`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/external/chainlink/ChainlinkUtil.sol#L32-L33) doesn't handle this case.

**Impact:** Code will execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for users.

**Recommended Mitigation:** Revert unless `minAnswer < answer < maxAnswer`.

**Zaros:** Fixed in commits [b14b208](https://github.com/zaros-labs/zaros-core/commit/c927d94d20f74c6c4e5bc7b7cca1038a6a7aa5e9) & [4a5e53c](https://github.com/zaros-labs/zaros-core/commit/4a5e53c9c0f32e9b6d7e84a20cc47a9f6024def6#).

**Cyfrin:** Verified.
