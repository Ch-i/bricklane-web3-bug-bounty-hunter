---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-11
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`Pricer` silently truncates `priceIds` to `uint80` which could map to incorrect
  Chainlink rounds'
vuln_class: []
---

# `Pricer` silently truncates `priceIds` to `uint80` which could map to incorrect Chainlink rounds

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `Pricer` silently truncates `priceIds` to `uint80` which could map to incorrect Chainlink rounds:
```solidity
Pricer.sol
161:        (, int256 answer,, uint256 updatedAt,) = $.priceFeed.getRoundData(uint80(priceId));
184:        (, int256 answer,, uint256 updatedAt,) = $.priceFeed.getRoundData(uint80(priceId));
211:            (, int256 answer,, uint256 updatedAt,) = $.priceFeed.getRoundData(uint80(_priceIds[i]));
```

**Recommended Mitigation:** Consider using [SafeCast::toUint80](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeCast.sol#L407-L412) to revert in such cases.

**Aarc:** Fixed in commit [48598d4](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/48598d40a4dec0f2ae661824c4bdf174b39d6e06).

**Cyfrin:** Verified.

\clearpage
