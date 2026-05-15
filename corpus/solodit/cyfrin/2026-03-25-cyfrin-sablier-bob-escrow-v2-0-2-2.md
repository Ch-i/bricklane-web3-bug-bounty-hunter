---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Immutable Curve pool dependency creates long-term redemption risk for adapter
  vaults
vuln_class: []
---

# Immutable Curve pool dependency creates long-term redemption risk for adapter vaults

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** `SablierLidoAdapter` uses an immutable `CURVE_POOL` address (`SablierLidoAdapter.sol:36`) as the **sole exit path** from stETH back to ETH during unstaking. The entire redemption flow for adapter vaults depends on this single Curve pool:

```solidity
// SablierLidoAdapter.sol:367-389 — the ONLY path from wstETH to WETH
function _wstETHToWeth(uint128 wstETHAmount) private returns (uint128 wethReceived) {
    uint256 stETHAmount = IWstETH(WSTETH).unwrap(wstETHAmount);
    uint256 expectedEthOut = ICurveStETHPool(CURVE_POOL).get_dy(1, 0, stETHAmount);
    uint256 minEthOut = ud(expectedEthOut).mul(UNIT.sub(slippageTolerance)).unwrap();
    uint256 ethReceived = ICurveStETHPool(CURVE_POOL).exchange(1, 0, stETHAmount, minEthOut);
    // ...
}
```

Bob vaults are designed to lock tokens for potentially long durations — years or even decades. During this time:

- `CURVE_POOL` is immutable; there is no setter or migration function
- There is no fallback exit path (e.g., Lido's native withdrawal queue)
- There is no admin rescue function to recover stuck wstETH
- There is no alternative DEX or liquidity source

If the specific Curve stETH/ETH pool referenced by `CURVE_POOL` loses liquidity, is deprecated, migrates to a new version, or becomes non-functional at any point during a vault's lifetime, all adapter vault redemptions permanently revert. The wstETH remains locked in the adapter with no recovery mechanism.

Notably, Lido introduced a native withdrawal queue (mid-2023) that provides a guaranteed 1:1 stETH→ETH exit without any DEX liquidity dependency. The adapter does not use this as either a primary or fallback path.

**Impact:** All adapter vaults become permanently unredeemable if the immutable Curve pool becomes unusable. The staked WETH (plus accumulated yield) is locked forever. This affects every user who entered an adapter vault, with no admin intervention possible.

The likelihood is low since the Curve stETH/ETH pool is one of the most established DeFi pools, but the 10-20 year vault horizons exceed the entire lifespan of DeFi to date. Any of the following could trigger the issue: Curve v1 deprecation, pool migration to Curve v2/v3, governance-mandated pool shutdown, or sustained liquidity drain.

**Recommended Mitigation:** Add Lido's native withdrawal queue as a fallback (or primary) unstaking path. This provides a guaranteed 1:1 exit that doesn't depend on any DEX liquidity:

```solidity
// Add as a fallback when Curve swap fails or as the primary path
ILidoWithdrawalQueue(WITHDRAWAL_QUEUE).requestWithdrawals(amounts, address(this));
// ... wait for finalization ...
ILidoWithdrawalQueue(WITHDRAWAL_QUEUE).claimWithdrawals(requestIds, hints);
```

Alternatively, make the Curve pool address updatable by the comptroller so it can be migrated to a new pool if the original is deprecated:

```solidity
function setCurvePool(address newPool) external onlyComptroller {
    curvePool = newPool;
    IStETH(STETH).approve(newPool, type(uint256).max);
}
```

**Sablier:** Fixed in commits:
* [f9c14e2](https://github.com/sablier-labs/lockup/commit/f9c14e2f6d4ba6a9d4309cb45408ba20e6a0d393) - integrating Lido native withdrawal
* [6ddfaac](https://github.com/sablier-labs/lockup/commit/6ddfaacf0f243fe3f15efa564c58719fa8a71d5e) - implement mitigation feedback to prevent vault unstaked via Curve from also being used to initiate Lido withdrawals

**Cyfrin:** Verified; there are now two exclusive options for redemption: Curve & Lido Withdrawals. For a given vault:
* if no Lido withdrawal has been initiated, any user can initiate a Curve redemption which prevents subsequent Lido withdrawals for the same vault
* if no Curve redemption has been initiated, the `Comptroller` can initiate a Lido Withdrawal which prevents Curve redemptions for the same vault
