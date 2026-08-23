---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Round up fee against users
vuln_class: []
---

# Round up fee against users

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Solidity by default rounds down, but generally fees should be rounded up against users. Using Solady's [library](https://github.com/Vectorized/solady/blob/main/src/utils/FixedPointMathLib.sol) is significantly more efficient than OpenZeppelin:
```solidity
import {FixedPointMathLib} from "@solady/utils/FixedPointMathLib.sol";

function _getFee() internal view returns (uint256 fee) {
    // read fee factor directly to output variable
    fee = s_feeFactor;

    // only do extra work if non-zero
    if(fee != 0) fee = FixedPointMathLib.fullMulDivUp(fee, PRICE_FEED_PRECISION, _getLatestPrice());
}
```

A secondary benefit of using the above is eliminating the possibility of revert due to [intermediate multiplication overflow](https://x.com/DevDacian/status/1892529633104396479), though in this code it isn't a real possibility.

If you don't want to round up against users but want a slightly faster implementation than the default:
```solidity
function _getFee() internal view returns (uint256 fee) {
    // read fee factor directly to output variable
    fee = s_feeFactor;

    // only do extra work if non-zero
    if(fee != 0) fee = (fee * PRICE_FEED_PRECISION) / _getLatestPrice();
}
```

**Evo:**
Fixed in commit [52c5384](https://github.com/contractlevel/sbt/commit/52c538448fbceb09f27ae657bcecb0c1483eb933).

**Cyfrin:** Verified.
