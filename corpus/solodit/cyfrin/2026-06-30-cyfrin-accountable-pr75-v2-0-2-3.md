---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableYield` still writes `lostAssets` and `lastTotalAssets` but no
  on-chain logic reads either after PR75 rewrote the fee path to a per-share HWM'
vuln_class: []
---

# `AccountableYield` still writes `lostAssets` and `lastTotalAssets` but no on-chain logic reads either after PR75 rewrote the fee path to a per-share HWM

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** The performance-fee computation in `_accruedFeeShares` derives the fee purely from a per-share high-water mark (`peakSharePrice`), with no reference to either `lostAssets` or `lastTotalAssets` - the two accumulators the pre-rewrite fee model relied on (an absolute total-assets baseline net of realized losses). A scope-wide trace finds both are still written but read nowhere on-chain: `publishRate` increments `lostAssets` on every reported loss (`src/strategies/AccountableYield.sol:230`), and `lastTotalAssets` is rewritten on every flow and accrual - `borrow` (`src/strategies/AccountableYield.sol:316`), `repay` (`src/strategies/AccountableYield.sol:363`), `onDeposit` (`src/strategies/AccountableYield.sol:426`), `onMint` (`src/strategies/AccountableYield.sol:452`), and `_accrueFees` (`src/strategies/AccountableYield.sol:507`) - yet the only non-write references to either are the auto-generated public view getters. Both are dead state. The `lostAssets` NatSpec ("Realized losses that should not generate fees on recovery") describes a fee-recovery-suppression role the current path implements through `peakSharePrice` instead, and the `lastTotalAssets += assets` form on the deposit and mint hooks pays an `SLOAD` plus `SSTORE` on every deposit for a value nothing consumes. There is no incorrect on-chain result today, since the per-share HWM provides recovery suppression up to the prior peak by construction. The risk is drift plus wasted gas: a maintainer who trusts the stale `lostAssets` comment may re-wire it back into the fee math alongside the HWM, double-counting the recovery suppression and under-charging fees, while every flow path keeps paying to maintain a `lastTotalAssets` baseline the rewrite abandoned.

**Recommended Mitigation:** Either remove both now-unused accumulators along with their writes (`lostAssets` in `publishRate`; `lastTotalAssets` in `borrow`, `repay`, `onDeposit`, `onMint`, `_accrueFees`), or document that under the per-share high-water-mark model both are retained only as observability figures and are not inputs to fee math. If `lostAssets` is kept, add a code comment at the `peakSharePrice`-based fee computation making explicit that recovery suppression is the HWM's responsibility and that `lostAssets` must not be re-introduced into the fee path. Removing storage from an upgradeable contract changes the slot layout, so do so only on a fresh deployment or with a deliberate slot-preserving migration.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
