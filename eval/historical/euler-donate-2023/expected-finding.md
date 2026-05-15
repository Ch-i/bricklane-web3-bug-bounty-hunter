---
id: euler-donate-2023
title: "Donate-without-healthcheck + unbounded liquidation discount → self-liquidation drain"
post_mortem_url: https://blog.euler.finance/euler-finance-incident-report-march-2023-4ed83b4d27d6
incident_date: "2023-03-13"
funds_at_risk_usd: 197000000
target_protocol: euler
expected_vuln_class:
  - business-logic
  - liquidation
  - missing-health-check
  - access-control
expected_severity: Critical
expected_locations:
  - file: CreditMarket.sol
    function: donateToReserves
  - file: CreditMarket.sol
    function: liquidate
required_keywords:
  - donateToReserves
  - liquidation
memorization_signals:
  - euler
  - "$197"
  - 197M
  - "2023-03"
exclude_corpus_ids: []
grading_mode: keyword
---

# Canonical bug

The bug is the *interaction* between two functions that each look fine in
isolation:

1. **`donateToReserves(amount)`** burns the caller's collateral and credits
   it to protocol reserves. The function checks that the donor has enough
   collateral to cover the donation — but **never calls `_requireHealth`
   on the donor afterwards**. A user can therefore voluntarily reduce
   their own collateral below the liquidation threshold while leaving
   their debt position open.

2. **`liquidate(violator, repayAmount)`** computes a liquidation discount
   that scales linearly with how far below the threshold the violator's
   health factor is — running from 0 bps at HF=threshold up to 10000 bps
   (100% bonus, i.e. 2× the repaid amount in seized collateral) at HF=0.
   The discount has **no upper cap independent of HF** and is not clamped
   to any fraction of the position size.

The exploit primitive:

1. Attacker deposits collateral and borrows up to the LTV cap.
2. Attacker calls `donateToReserves` with enough collateral that they
   become liquidatable. The protocol allows this because the health
   check is missing on `donateToReserves`.
3. An accomplice (or a flash-loan-funded second account controlled by
   the same attacker) calls `liquidate(attacker, repayAmount)` and
   receives `repayAmount + bonus` worth of collateral at the inflated
   discount. With a steep enough discount, the value extracted by the
   liquidator exceeds the attacker's donation. Real Euler amplified this
   asymmetry via eToken/dToken share recursion; even without share
   recursion the missing health check + unbounded discount is a
   stand-alone Critical finding.

This is the **structural shape** of the March 2023 Euler exploit
(~$197M). The faithful detail in Euler was that `donateToReserves`
operated on eTokens (interest-bearing share representations) which made
the share-math asymmetry exploitable for net positive profit; the
present contract is a 1:1-collateral simplification of the same
liability surface.

## Why an auditor should catch this

- `donateToReserves` (lines ~88-93) mutates collateral but never calls
  `_requireHealth(msg.sender)`. Every other state-mutating function
  that decreases collateral or increases debt does call the health
  check. The omission is what turns "donate to a protocol" into "make
  yourself liquidatable on demand".

- `_liquidationDiscountBps` (lines ~155-162) ramps unboundedly toward
  10000 bps as HF approaches 0. There's no per-call cap on the bonus,
  no requirement that the liquidator be different from the violator,
  and no `whenSolvent` guard on the violator's donation pathway. Any
  positive discount at HF below threshold means a self-liquidation
  with an accomplice can net positive value relative to the donation.

- The `clearBadDebt` function (lines ~135-142) lets *anyone* clear the
  residual debt of a bankrupt user against reserves — this is a
  secondary access-control oversight. A passing audit should at least
  note this even if it doesn't reach the donate-liquidate combination.

## Acceptance criteria for the eval

A passing finding must:

1. Identify the missing health check in `donateToReserves` (the
   `donateToReserves` keyword is required for the match).
2. Relate the missing health check to the `liquidate` flow — i.e.
   the auditor must connect the two functions, not just flag
   `donateToReserves` in isolation (the `liquidation` keyword is
   required for the match).
3. Be rated Critical or High.

Findings that only spot the unbounded discount (without the donate
linkage) or only the missing health check (without the liquidation
linkage) fail this eval — the value of the entry is precisely that it
requires *cross-function reasoning*.
