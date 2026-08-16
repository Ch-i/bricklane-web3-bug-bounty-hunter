---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-0-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableYield` lacks an `InDefaultClaims` wind-down and permanently strands
  unfulfilled redemptions after a default'
vuln_class: []
---

# `AccountableYield` lacks an `InDefaultClaims` wind-down and permanently strands unfulfilled redemptions after a default

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** This finding is outside the PR75 change set - the default lifecycle, the redemption hooks, and `_sharePrice` are pre-existing `AccountableYield` and `AccountableStrategy` code, not the PR75 diff - and is included because it materially affects depositor funds.

When a loan default is accepted, `loanState` leaves the ongoing states and `publishRate` can no longer run, because it begins with `_requireLoanOngoing` (`src/strategies/AccountableYield.sol:213`). `publishRate` is the only writer of `navGraceDeadline`, so within the grace period (`DEFAULT_NAV_GRACE_PERIOD`, up to 24 hours) `_navIsStale` becomes permanently true and can never be cleared. From that point a redemption that has not already been fulfilled can never be fulfilled, because all three fulfillment routes are dead:

1. Instant fulfillment in `requestRedeem` requires `!_navIsStale()` in `onRequestRedeem` (`src/strategies/AccountableYield.sol:473`), which is false, so the request only queues.
2. Queue processing through `vault.processUpToShares` is reachable only via `_processAvailableWithdrawals`, called solely by `repay` and `accrueAndProcess` (`src/strategies/AccountableYield.sol:365`, `src/strategies/AccountableYield.sol:400`), both of which carry `whenNotStale` and `_requireLoanOngoing` and therefore revert.
3. `AccountableYield` does not implement the `InDefaultClaims` wind-down its sibling strategies provide. `AccountableFixedTerm` and `AccountableOpenTerm` reprice `_sharePrice` to `IAccountableVault::assetShareRatio` and allow instant non-NAV-gated redemption in the `Repaid` and `InDefaultClaims` states, but `AccountableYield` overrides neither path and never reads `InDefaultClaims` at all.

`InDefaultClaims` is terminal - there is no transition back to an ongoing state - so the staleness and the resulting freeze are permanent absent a contract upgrade.

**Files:**

- `AccountableYield::publishRate, onRequestRedeem, coverDefault` (`src/strategies/AccountableYield.sol`)
- `AccountableYield::_processAvailableWithdrawals, _sharePrice` (`src/strategies/AccountableYield.sol`)
- `AccountableAsyncRedeemVault::requestRedeem, redeem, withdraw` (`src/vault/AccountableAsyncRedeemVault.sol`)

**Impact:** Depositors whose redemptions are not fulfilled before the NAV goes stale are permanently unable to redeem their shares for assets. The safety-module coverage injected through `coverDefault` - the capital specifically provided to backstop holders during a default - is unreachable for that cohort, because reaching it requires fulfillment (reserving liquidity against the queue), which is the blocked step. `cancelRedeemRequest` only returns the escrowed shares, not assets, so it is not an exit. The loss is bounded: redemptions already fulfilled remain claimable at any time, and during the brief post-default window before `navGraceDeadline` lapses holders can still exit via instant fulfillment against the remaining reserves and the coverage, though at the un-written-down `_sharePrice` and first-come-first-served, which lets early exiters over-extract. So the impact is permanent loss of access for late or illiquid redemptions during exactly the scenario the coverage mechanism exists to handle, rather than outright theft. Triggering it requires a default to be initiated (a privileged `defaultLoan` plus the permissionless `acceptDefault` after the one-day timer), but the presence of `coverDefault` shows defaults are a designed-for path.

**Recommended Mitigation:** Implement the `InDefaultClaims` wind-down the sibling strategies already have: in `_sharePrice` return `IAccountableVault(vault).assetShareRatio()` when `loanState` is `Repaid` or `InDefaultClaims`, and allow instant non-NAV-gated redemption in those states (mirroring `_isInstantRedeem` and `_requireCanRequestRedeem`). This lets depositors claim their pro-rata share of the remaining real assets, including the `coverDefault` coverage, at the recoverable basis regardless of NAV staleness. Alternatively, if `AccountableYield` is never intended to enter default, disable the inherited default entrypoints (`defaultLoan`, `coverDefault`, and the base `acceptDefault`) the same way `prepay` and `pay` are disabled with `revert NotSupportedByStrategy()`, so the unhandled terminal state is unreachable.

**Accountable:** Fixed in commit [`22bf5d5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/22bf5d58fc104094375b82ac7e39aac3ce6dd12b)

**Cyfrin:** Verified. Instant redeem allowed when `loanState` is in `InDefaultClaims`.
