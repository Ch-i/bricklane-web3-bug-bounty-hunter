---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-0-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md
tags:
- firm:codespect
- report:2026-07-02-hyperwave-sub-account-strategy-framework
title: '[L-03] withdraw(...) slippage floor misprices staker shares when unstake is
  true'
vuln_class: []
---

# [L-03] withdraw(...) slippage floor misprices staker shares when unstake is true

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [YieldBasisDecoderAndSanitizer.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/DecodersAndSanitizers/hyperwave/aprimeusd/YieldBasisDecoderAndSanitizer.sol)

**Description:**

The `withdraw(uint256 poolId, uint256 shares, uint256 minAssets, bool unstake, address receiver, bool withdrawStablecoins)` decoder derives its slippage floor from [`preview_withdraw(shares)`](https://github.com/yield-basis/yb-core/blob/master/contracts/LT.vy), which interprets `shares` as LT shares. `unstake` is read but ignored and not bound in the merkle leaf, so a strategist can call `withdraw` with `unstake = true`, where [`shares` is denominated in staker (gauge) shares](https://github.com/yield-basis/yb-core/blob/master/contracts/HybridVault.vy#L482) instead of LT shares.

**Impact:** The configured staker (`0xd829456FD63Ada7DE0657714A3A7A26DE403E3D8`) is a non-1:1 ERC4626 vault over the LT (`convertToAssets(1e18) ≈ 0.985` LT, drifting as rewards accrue). With `unstake = true` the decoder prices staker shares as LT shares, overstating the withdrawal, so `minAllowed` is too high and the strategist must set `minAssets` above what the smaller actual LT withdrawal can deliver, reverting the call. No funds are at risk since the LT still enforces the strategist’s `minAssets`; this blocks the staked-withdrawal path through the decoder and requires the position to have been staked first.

**Recommendation:** Bind `stake` / `unstake` in the merkle leaf so the decoder only authorizes the unstaked domain its floor assumes; if staked withdrawals are required, convert staker shares to LT shares via the staker’s `convertToAssets(...)` before calling `preview_withdraw(...)`.

**Status:** Fixed

**Client response:** fixed in [PR-87](https://github.com/SwellNetwork/boring-vault/pull/87).

**CODESPECT fix review:** Fixed in commit [`bcfacae`](https://github.com/SwellNetwork/boring-vault/commit/bcfacae4894eebabcaee2bee076d0336418ea07b).
