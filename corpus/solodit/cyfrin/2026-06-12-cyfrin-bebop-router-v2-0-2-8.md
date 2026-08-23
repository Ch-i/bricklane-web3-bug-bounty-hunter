---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: BebopRouter::swap exactOut does not require a negative limitAmount, leaving
  input pulls without an order-committed max-spend ceiling
vuln_class: []
---

# BebopRouter::swap exactOut does not require a negative limitAmount, leaving input pulls without an order-committed max-spend ceiling

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** In exactOut mode (`exactAmount < 0`), `_calculateAmounts` computes `newFromAmount = order.fromAmount * newToAmount / order.toAmount` (line 422) and then applies a cap at line 423: `require(order.limitAmount >= 0 || newFromAmount <= uint256(-order.limitAmount))`. When `order.limitAmount >= 0`, this require is trivially satisfied for all values of `newFromAmount` - the cap never applies.

`settle` guards against this asymmetry with an explicit check at line 205 (`require(exactAmount > 0 || order.limitAmount < 0)`), which forces exactOut settle callers to declare a maximum spend via a negative `limitAmount`. `swap` has no equivalent guard. An order signed with `exactAmount < 0` and `limitAmount >= 0` in the `swap` path has no on-chain ceiling on the input pulled from `msg.sender`, bounded only by the taker's standing approval to the router.

While the input comes from `msg.sender` (the taker funds themselves), a signer-authored order with an adverse order ratio (`order.fromAmount / order.toAmount` significantly higher than the PMM ratio) can compute a `newFromAmount` far exceeding what a taker would expect for the stated exactOut target, with no signed maximum spend to protect them.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::swap` (line 205 - the guard present in `settle` but absent in `swap`)
- `contracts/BebopRouter.sol` - `BebopRouter::_calculateAmounts` (line 423)

**Impact:** The taker in `swap` exactOut has no signed ceiling on the input token pulled when `limitAmount >= 0`. The protection the design intends for exactOut - "never overpays" - relies on `limitAmount < 0` as the signed maximum-spend commitment. Without enforcing this for `swap`, a routerSigner-authored order with an inflated order ratio can pull significantly more `fromToken` from the taker than the stated exactOut fill warrants. The harm is bounded to the taker's own approval and is self-inflicted in the sense that `msg.sender` is paying, but the signer controls the ratio.

**Recommended Mitigation:** Add the same guard that `settle` applies: `require(exactAmount > 0 || order.limitAmount < 0, LimitAmountRequiredForExactOut())` at the start of `swap`. This ensures exactOut swap callers always provide a signed spend ceiling via a negative `limitAmount`, consistent with the documented exactOut never-overpays intent.

**Bebop:** Acknowledged. Exact-out swap permits no ceiling because the caller funds and submits the transaction; settle retains the mandatory signed ceiling.
