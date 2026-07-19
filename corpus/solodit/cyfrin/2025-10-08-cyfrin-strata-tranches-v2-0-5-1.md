---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-5-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Cache result of external calls when result can't change between calls and is
  used multiple times
vuln_class: []
---

# Cache result of external calls when result can't change between calls and is used multiple times

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** * `Tranche.sol`
```solidity
// configure
212:        IERC20[] memory tokens = cdo.strategy().getSupportedTokens();
213:        uint256 len = tokens.length;
214:        address strategy = address(cdo.strategy());
```

**Recommended Mitigation:**
```diff
++import { IStrategy } from "./interfaces/IStrategy.sol";
[…]
    function configure () external onlyCDO {
--      IERC20[] memory tokens = cdo.strategy().getSupportedTokens();
--      uint256 len = tokens.length;
--      address strategy = address(cdo.strategy());
++      address strategy = address(cdo.strategy());
++      IERC20[] memory tokens = IStrategy(strategy).getSupportedTokens();
++      uint256 len = tokens.length;
```

**Strata:**
Fixed in commit [732b1a8](https://github.com/Strata-Money/contracts-tranches/commit/732b1a8ee5ae0bda763f74556f89bbb28b63f784) by caching the result of the call `cdo::strategy` and re-using it.

**Cyfrin:** Verified.

\clearpage
