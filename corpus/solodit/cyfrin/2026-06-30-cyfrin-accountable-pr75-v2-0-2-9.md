---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: Redemptions are priced at the live NAV with no front-running protection, unlike
  deposits, letting a holder exit ahead of a NAV-loss publish
vuln_class: []
---

# Redemptions are priced at the live NAV with no front-running protection, unlike deposits, letting a holder exit ahead of a NAV-loss publish

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** The protocol batches deposits through `DepositGateway` so they "enter `AccountableYield` only at the post-NAV price": a depositor commits capital before the NAV that prices them is known and therefore cannot front-run a NAV move. Redemptions have no equivalent guard. `onRequestRedeem` prices a redemption at the live `_sharePrice` and instant-fulfills it in the same transaction whenever liquidity is available and the NAV is not stale:

```solidity
function onRequestRedeem(address share, uint256 shares, address, address)
    public override(AccountableStrategy, IStrategyVaultHooks) nonReentrant onlyVault whenNotPaused
    returns (bool canFulfill, uint256 price)
{
    if (shares < _loan.minRedeem) revert InsufficientShares();
    _accruePenalties();
    _accrueFees();
    price = _sharePrice(share);
    uint256 assets = shares.mulDiv(price, PRECISION);
    uint256 liquidity = _getAvailableLiquidity();
    canFulfill = liquidity >= assets && !_navIsStale();
}
```

`_navIsStale()` is false for the entire `navGracePeriod` (default 24h) after the last publish, so a redemption is priced at the last published NAV right up until the next `publishRate` overwrites it:

```solidity
function _navIsStale() internal view returns (bool) {
    return block.timestamp > navGraceDeadline;
}
```

`publishRate` is a single, mempool-visible transaction whose `newDeployedValue` fully determines the new (lower) share price:

```solidity
function publishRate(uint256 newDeployedValue, uint256 measuredAt) external {
    if (msg.sender != dvnPublisher) revert Unauthorized();
    _requireLoanOngoing();
    // ...
    deployedAssets = newDeployedValue;
    // ...
}
```

A holder who sees a pending loss publish (a `publishRate` with a lower `newDeployedValue` sitting in the mempool, or a foreseeable delinquent-borrower NAV drop) can `requestRedeem` first; with vault liquidity available the request instant-fulfills at the current pre-loss price, and the published loss then falls entirely on the remaining holders. This is the exit-side mirror of the front-running the deposit gateway exists to prevent on the entry side.

**Impact:** A holder who front-runs a NAV-loss publish redeems at the stale pre-loss price while vault liquidity lasts, extracting value from and shifting the marked-down loss onto the remaining holders, the exact attack the deposit gateway blocks on entry but which has no equivalent guard on exit.

**Proof of Concept:**
1. Vault has 1,000,000 shares, `deployedAssets = 800,000`, idle vault liquidity 300,000, share price 1.10. The NAV is about to be marked down to 600,000 (fair price 0.90).
2. The `dvnPublisher` broadcasts `publishRate(600_000, ...)`; the transaction sits in the mempool.
3. Eve front-runs it with `requestRedeem(272_727 shares)`. `onRequestRedeem` prices at the live 1.10 so `assets = 300_000`; `liquidity (300_000) >= 300_000` and the NAV is not yet stale, so `canFulfill = true` and the request is instant-fulfilled.
4. Eve receives 300,000 assets for shares worth 245,454 at the fair post-loss price.
5. `publishRate(600_000)` lands; the ~54,545 shortfall is absorbed by the remaining 727,273 holders.

**Recommended Mitigation:** Apply the same post-NAV pricing discipline to the exit side that the gateway provides on entry: route instant redemptions through a batch/queue that prices at the next published NAV rather than the last one, or block instant fulfillment within a window around a pending NAV update. At a minimum, bound the exposure with a shorter `navGracePeriod` and per-window liquidity caps so the amount that can exit at a stale price before a loss is published is limited.


**Accountable:** Fixed in commit [`0f7abda`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/0f7abda88e294c13dd1e30d1a57d9b219b4846a6) — gates the permissionless `accrueAndProcess` on `instantRedeemMaxAge`.

**Cyfrin:** The `maxAge` gate now covers both the instant path and the permissionless `accrueAndProcess` (which skips processing once the NAV is older than `maxAge`), so a redeemer can no longer `requestRedeem` then `accrueAndProcess` to settle at the stale NAV. Two residuals are accepted as Informational since impact is bounded by available liquidity: the borrower's `repay` still processes the queue ungated, and disabled mode (`maxAge = type(uint256).max`) leaves `accrueAndProcess` ungated, so protection holds only in windowed mode (`0 < maxAge < navGracePeriod`
