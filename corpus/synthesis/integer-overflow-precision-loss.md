---
id: synthesis-integer-overflow-precision-loss
source: synthesis
source_url: null
title: "Integer Overflow & Precision Loss: pattern, variants, audit checklist"
ingested_at: 2026-06-04T20:04:09Z
vuln_class:
  - integer-overflow
  - rounding
  - precision-loss
  - accounting
  - dos
protocol_category:
  - defi
  - amm
  - lending
  - vault
  - staking
tags:
  - synthesis
  - integer-overflow
  - rounding
  - precision-loss
  - dust
derives_from:
  - swc-101
  - rekt-balancer-rekt2
  - rekt-bunni-rekt
  - rekt-sss-rekt
  - arxiv-2603.00890
  - solodit-zokyo-2024-11-19-tren-1-1
  - solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-0
  - solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-1
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-1
  - solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-9
  - solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-7
  - solodit-auditone-2023-06-29-coinlend-0-5
  - solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-0
  - solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-2
  - solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-2-1
---

# Integer Overflow & Precision Loss

## Pattern

Smart contracts do all of their accounting in fixed-width unsigned integers
with no native fractional type. Two distinct failure families fall out of this:

**Overflow / underflow.** An arithmetic result that escapes the range of its
type (e.g. `0 - 1` on a `uint`, or `a * b` exceeding `2^256-1`) wraps around or
reverts. Before Solidity 0.8 this wrapping was silent; the canonical example is
`map[k] -= v` underflowing a balance to a huge number (SWC-101). Solidity 0.8+
checks arithmetic by default, but the same wrap-around is still reachable inside
`unchecked { ... }` blocks, in narrowing casts (`toUint128`, `uint8(x)`), in
inline assembly, and in hand-rolled "cascading" subtraction where a computed
remainder can exceed the value it is subtracted from. The Super Sushi Samurai
mint exploit is an accounting-overflow cousin: a transfer that subtracted from
the sender before adding to the recipient *doubled* a balance when sender and
recipient were the same address.

**Precision / rounding loss.** Because integer division truncates toward zero,
every `/` discards a remainder. Individually each lost wei looks like harmless
"dust," but the direction and ordering of rounding decide *who* absorbs the
loss. Three things turn dust into a vulnerability: (1) **ordering** — dividing
before multiplying amplifies truncation (`(apy/100)*amount` loses far more than
`(apy*amount)/100`); (2) **direction** — rounding in favor of the user instead
of the protocol leaks value on every interaction and violates the
mint-up / redeem-down discipline EIP-4626 prescribes; and (3) **rounding to
zero** — when the truncated result collapses to `0`, an attacker can extract
value for free or wedge the protocol into a DoS.

For an auditor, the tell is any expression that mixes `*`, `/`, decimal scaling
(`10**(18-d)`, `/1e18`, WAD/RAY), and a value that an attacker controls the
*size* of. Ask: what is the remainder, which direction does it round, who keeps
it, and can the attacker make the numerator small enough (or the divisor large
enough) to force the result to zero? Note also that automated tooling is weak
here: a benchmark of Mythril, Oyente and Slither on integer-arithmetic errors
(among other classes) found F1 scores ranging from 31% to 95% with
false-positive rates up to ~33% — meaning overflow/precision findings cannot be
delegated to static analyzers and need manual reasoning about magnitudes.

## Variants

### V1: Unchecked overflow / underflow and unsafe casts

The classic SWC-101 case: arithmetic that wraps when it leaves type bounds.
Reachable via pre-0.8 code, `unchecked` blocks, narrowing casts, assembly, and
hand-written subtraction over computed remainders. In Suzaku's slashing logic a
remainder-derived `nextWithdrawalsSlashed` could exceed `nextWithdrawals`,
making `nextWithdrawals - nextWithdrawalsSlashed` underflow and revert — a DoS
on the slashing mechanism that an attacker can deliberately engineer
[solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2]. Super Sushi Samurai is
the value-extraction face of the same family: balance accounting that didn't
handle the self-transfer edge case let a holder double their balance and mint
$4.8M of sellable tokens [rekt-sss-rekt, swc-101].

### V2: Division before multiplication

Performing `/` before `*` truncates the intermediate, so the final result is
systematically too small. `((apy / 100) * investmentAmount) / timePeriod` rounds
`apy/100` down first and understates emissions, hurting users with low APY
[solodit-zokyo-2024-11-19-tren-1-1]. swETH's `reprice` did
`percentage.div(total).mul(rewards)`, losing precision on node-operator rewards;
the fix is simply to multiply first then divide
[solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-0].

### V3: Wrong rounding direction (value leaks to the wrong party)

When the rounding direction favors the user rather than the protocol, value
leaks on every transaction. Securitize's `executeBuyBase` floored `execPrice`
when scaling WAD → token decimals, so buyers always paid slightly *less* than the
true price [solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-9].
YieldFi's `previewMint` / `previewWithdraw` rounded in the user's favor,
contradicting EIP-4626 security guidance (mint/withdraw should round against the
user) [solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-2]. At protocol scale this
is exactly what destroyed Balancer V2: a `_upscale()` scaling function that
*always* rounded one direction (down) — a developer had even commented the error
was "expected to be minimal" — let an attacker manipulate rates for a $128M loss,
which several forks inherited via copy-paste [rekt-balancer-rekt2].

### V4: Truncation-to-zero (free value or DoS)

A stronger form of V3: the truncated quotient collapses to `0`. Sablier's
`SablierLidoAdapter` computed `fromWstETH * shareAmount / userShareBalance` with
floor division; because the wstETH:share rate is below 1:1, a 1-wei share
transfer rounds the wstETH-to-move to `0`, letting a sender hand out shares while
keeping all backing — recipients get worthless shares
[solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-2-1]. Symbiotic's
decimal normalizer divides high-decimal stakes by `10**(decimals-24)`, so any
stake below the divisor yields *zero* voting power, silently disenfranchising
legitimate stakeholders [solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-1].
Coinlend's LTV divided by `1e18` and could round the ratio to `0`, preventing
liquidations that should have fired and putting lender funds at risk
[solodit-auditone-2023-06-29-coinlend-0-5].

### V5: Dust accumulation / permanently locked remainders

Truncated remainders that no one can recover. Paladin Valkyrie computed
`ratePerSec = amount / duration`; with low-decimal high-value tokens (e.g.
8-decimal WBTC) the lost dust — and its amplification when extending the
distribution — leaves meaningful value stuck forever
[solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-7]. Myriad's
`redeemVoided` truncated `balance * payoutRatio / 1e18`, permanently locking the
remainder with no recovery path; the remediation is a dust-sweep admin function
or documented behavior [solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-1].

### V6: Decimal-scaling mismatch (hardcoded 18 decimals)

Code that assumes every token is 18 decimals miscalculates for 6-decimal
(USDC/USDT) or >24-decimal tokens. OctoDeFi's `calculateFee` divided by `1e18` to
cancel the oracle's scaling but ignored the token's own decimals, so a USDT fee
came out `1e12×` too small and summing fees across mixed-decimal tokens added
incommensurable units [solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-0]. The
same `decimals`-blind scaling drives the rounding-to-zero in Symbiotic above
[solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-1].

### V7: Compounding precision in custom curve / rebalancing math

Bespoke pricing math compounds tiny rounding errors into exploitable drift.
Bunni's custom Liquidity Distribution Function had a "basic rounding bug" in its
rebalancing logic: carefully sized trades broke the math at the right moments and
allowed repeated withdrawals draining $8.4M — no flash loan or oracle
manipulation required [rekt-bunni-rekt]. This is V2–V4 combined inside novel
math that lacked the rounding invariants of standard AMM curves.

## Audit checklist

- Is every `unchecked` block, narrowing cast (`toUintN`, `uintN(x)`), and
  assembly arithmetic provably within bounds for all attacker-controlled inputs?
  [swc-101, solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2]
- Does any subtraction operate on a *computed remainder* that could exceed the
  value being subtracted from (cascading slashing/fee logic)?
  [solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2]
- Are sender == recipient and other self-referential edge cases handled in
  balance/transfer accounting? [rekt-sss-rekt]
- Does every expression multiply before it divides (no division feeding a later
  multiplication)? [solodit-zokyo-2024-11-19-tren-1-1,
  solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-0]
- For each `/`, which direction does it round, and does that direction favor the
  protocol rather than the user (mint/deposit-conversion up, redeem/withdraw
  down per EIP-4626)? [solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-2,
  solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-9,
  rekt-balancer-rekt2]
- Is the scaling/`_upscale`-style helper bidirectional (round up *and* down where
  appropriate) rather than always rounding one way? [rekt-balancer-rekt2]
- Can a truncated result reach zero for small amounts, and would a zero result
  grant free value or revert into a DoS? Are there minimum-amount guards?
  [solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-2-1,
  solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-1,
  solodit-auditone-2023-06-29-coinlend-0-5]
- Is token `decimals()` read from the asset instead of hardcoded to 18, and are
  values in the same unit before they are added? [solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-0]
- Is there an unnecessary `/1e18` (or WAD/RAY) division that could be cancelled
  algebraically to preserve precision? [solodit-auditone-2023-06-29-coinlend-0-5]
- Where remainders are unavoidable, is there a dust-sweep / recovery path, or is
  the rounding behavior at least documented? [solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-1,
  solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-7]
- For low-decimal / high-value tokens (WBTC 8d, USDC 6d) and high-decimal
  tokens (>24d), is per-second / per-share rate precision still adequate?
  [solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-7,
  solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-1]
- For custom pricing/curve/rebalancing math, do rounding invariants hold under
  repeated and adversarially-sized trades (not just average-case)? [rekt-bunni-rekt]
- Are overflow/precision findings reasoned about manually rather than relying on
  static analyzers, given their high false-positive / variable accuracy on this
  class? [arxiv-2603.00890]

## Prior incidents

- **Balancer V2 (Composable Stable Pools) — Nov 3 2025 — $128M**: the `_upscale()`
  scaling function rounded in only one direction (down), letting an attacker
  manipulate pool rates; several forks inherited the copy-pasted bug
  [cites: rekt-balancer-rekt2].
- **Bunni — Sep 1 2025 — $8.4M**: a rounding bug in the custom Liquidity
  Distribution Function's rebalancing logic let precisely sized trades enable
  repeated withdrawals; no flash loan or oracle manipulation needed
  [cites: rekt-bunni-rekt].
- **Super Sushi Samurai (Blast L2) — Mar 21 2024 — $4.8M**: transfer accounting
  failed the self-transfer case, doubling a balance and enabling an infinite-mint
  drain of the LP [cites: rekt-sss-rekt].

## References

- corpus entries (also in `derives_from`):
  - swc-101 — SWC-101: Integer Overflow and Underflow
  - rekt-balancer-rekt2 — Balancer Rekt II ($128M, one-direction rounding in `_upscale`)
  - rekt-bunni-rekt — Bunni Rekt ($8.4M, LDF rounding bug)
  - rekt-sss-rekt — Super Sushi Samurai REKT ($4.8M, self-transfer accounting overflow)
  - arxiv-2603.00890 — Where Do Smart Contract Security Analyzers Fall Short? (integer-arithmetic detection limits)
  - solodit-zokyo-2024-11-19-tren-1-1 — Precision loss: division before multiplication
  - solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-0 — swETH reprice division-before-multiplication
  - solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-1 — High-decimal stake rounds to zero voting power
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2 — Underflow in cascading slashing logic (DoS)
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-1 — Dust permanently locked via truncation
  - solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-9 — Wrong rounding direction favors buyer
  - solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-7 — Precision loss locks reward dust
  - solodit-auditone-2023-06-29-coinlend-0-5 — LTV rounds to zero, blocks liquidation
  - solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-0 — Fee math assumes 18 decimals
  - solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-2 — previewMint/previewWithdraw round toward user
  - solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-2-1 — Floor division to zero detaches share backing
