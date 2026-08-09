---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: '`SolidlyV3Pool::_mint` and `_swap` don''t verify tokens were actually received
  by the pool'
vuln_class: []
---

# `SolidlyV3Pool::_mint` and `_swap` don't verify tokens were actually received by the pool

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Some versions of [`SolidlyV3Pool::_mint`](https://github.com/SolidlyV3/v3-core/blob/main/contracts/SolidlyV3Pool.sol#L288-L291) & [`_swap`](https://github.com/SolidlyV3/v3-core/blob/callbacks/contracts/SolidlyV3Pool.sol#L644-L650) don't verify tokens were actually received by the pool. In contrast UniswapV3's equivalent [`mint`](https://github.com/Uniswap/v3-core/blob/main/contracts/UniswapV3Pool.sol#L483-L484) & [`swap`](https://github.com/Uniswap/v3-core/blob/main/contracts/UniswapV3Pool.sol#L777-L783) functions always verify tokens were received by the pool.

**Impact:** Solidly will be more vulnerable to malicious tokens or tokens with non-standard behavior. One possible attack path is a token which has a blacklist that doesn't process transfers for blacklisted accounts but also doesn't revert and simply returns `true`. The token owner can execute a more subtle rug-pull by:
* allowing the pool to grow to a sufficient size
* adding themselves to the blacklist
* calling `swap` to drain the other token without actually transferring any of the malicious token, draining the liquidity pool.

**Recommended Mitigation:** `_mint` and `_swap` functions should check that the expected token amounts were transferred into the pool.

**Solidly:**
We ommited this on purpose for gas savings since we don't support exotic ERC20s on v3-core. Users can create such a pool if they want since it's permission-less, but it's something we explicitly and officially don't support.
