---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Initialization to zero price can cause permanent stuck state due to clamping
vuln_class: []
---

# Initialization to zero price can cause permanent stuck state due to clamping

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** In `ChainlinkOracle` in the constructor, the contract initializes `currentPriceX96`, `lastPriceX96`, and `emaPrice` using the current `sqrtPriceX96` from the Uniswap V4 pool. If the pool is uninitialized (`sqrtPriceX96 == 0`), all these price variables are set to zero. In this state, the `update` function will always clamp any new price to the range `lastPriceX96 ± (lastPriceX96 >> 6)`, which evaluates to `0 ± 0 = 0`. As a result, the oracle is stuck at zero and cannot update to a non-zero price, even if the pool becomes initialized later.

**Impact:** The oracle will be permanently stuck at a zero price if deployed before the pool is initialized. This prevents the oracle from ever reflecting the true market price, breaking all dependent pricing and margin logic. Users and protocols relying on the oracle will receive invalid (zero) price data, potentially causing loss of functionality or incorrect behavior.

**Recommended Mitigation:** Add a check in the constructor (and/or in the `update` function) to ensure that initialization only occurs if `sqrtPriceX96 > 0`. If the pool is uninitialized, revert deployment or defer initialization until a valid price is available. Alternatively, allow the oracle to update from zero to a non-zero price once the pool is initialized, bypassing the clamp logic when `lastPriceX96 == 0`.

**Licredity:** Fixed in [PR#16](https://github.com/Licredity/licredity-v1-oracle/pull/16/files), commit [`6f5fdd7`](https://github.com/Licredity/licredity-v1-oracle/commit/6f5fdd7c2fdffc4e90b80d7b1c967a700bc9936e)

**Cyfrin:** Verified. `sqrtPrice` now verified to not be `0` in the constructor.
