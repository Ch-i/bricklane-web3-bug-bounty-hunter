---
id: synthesis-auction-mechanisms-dutch-english
source: synthesis
source_url: null
title: "Auction Mechanisms (Dutch, English, Sealed-Bid): pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00+00:00
vuln_class:
  - rounding
  - precision-loss
  - accounting
  - dos
  - cei-violation
  - mev
  - front-running
  - input-validation
  - fee-on-transfer
protocol_category:
  - auction
  - nft-marketplace
  - amm
  - defi
tags:
  - synthesis
  - auction
  - dutch-auction
  - english-auction
  - sealed-bid
  - bid-settlement
derives_from:
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-0
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-1
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-2
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-1-0
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-0
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-1
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-3
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-0
  - solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-1
  - solodit-zokyo-2022-11-16-onemind-0-0
  - solodit-zokyo-2022-11-16-onemind-2-0
  - solodit-zokyo-2022-11-16-onemind-3-1
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-6
  - solodit-cyfrin-2023-06-01-sudoswap-1-2
  - solodit-guardian-audits-2023-04-08-nftr-0-1
  - solodit-guardian-audits-2023-04-08-nftr-0-3
  - solodit-guardian-audits-2023-04-08-nftr-1-3
  - solodit-pashov-audit-group-2023-02-01-punk-bid-0-1
  - swc-114
  - rekt-treasure-dao-rekt
  - arxiv-2603.07716
---

# Auction Mechanisms (Dutch, English, Sealed-Bid)

## Pattern

On-chain auctions are price-discovery state machines that combine three
fragile ingredients: a **time-dependent price/eligibility curve**, a
**bid-settlement accounting step**, and an **adversarial mempool** in
which the order of transactions is observable and manipulable. Almost
every auction bug in the corpus is a failure in one of these three
layers, and the bug class is largely independent of the auction flavor:

- **Dutch / Gradual Dutch Auctions (GDA):** price starts high and decays
  over time; the first bidder willing to pay the *current* computed price
  wins. The dangerous surface is the decay math itself — integer division
  ordering, precision loss, elapsed-time computation, and missing price
  bounds (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-2`,
  `...-2-1`, `solodit-cyfrin-2023-06-01-sudoswap-1-2`).
- **English auctions / bid books:** price ascends as bidders outbid each
  other; the highest standing bid at expiry wins, and superseded bids must
  be refundable. The dangerous surface is bid replacement, refunds, and
  griefing (`solodit-guardian-audits-2023-04-08-nftr-0-3`, `...-1-3`,
  `solodit-pashov-audit-group-2023-02-01-punk-bid-0-1`).
- **Sealed-bid auctions:** bids are meant to be hidden until reveal. On a
  transparent ledger this only works with a commit-reveal scheme; a naive
  "sealed" bid stored in calldata or state is fully visible, and
  whoever orders transactions can react to it (`swc-114`,
  `arxiv-2603.07716`).

The recurring economic failure is that value silently leaks from the
party the protocol intended to protect. In Dutch auctions, integer
division in `volume / price` rounds the winning bidder's claim *down*
while the seller keeps the full payment, so a remainder is pure loss to
the bidder, and with low-decimal purchase tokens the claim can round to
zero — a 100% loss
(`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-1`,
`...-1-0`). The same class of rounding/ordering error appears in the
price curve itself (`...-2-1`).

The second recurring failure is **lifecycle integrity**: the auction
state machine has start/end times, a finalize/settlement step, and a
"no bids" terminal state, and each transition must be validated and
atomic. Missing input validation on timestamps can strand reserves or
make an auction that never ends or never starts
(`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-0`);
splitting fee-payment and finalize lets the auction account be closed
before the NFT is delivered to the winner
(`solodit-zokyo-2022-11-16-onemind-0-0`); and an auction that ends with
no bids can permanently lock the listed tokens if there is no recovery
path (`solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-6`).

The third recurring failure is **transaction-order / mempool
dependence**. Bidding is inherently a race: an observer can see a pending
bid and react to it (`swc-114`). This manifests as front-running of
reveals in sealed-bid designs, last-block sniping in English auctions,
griefing by placing-then-withdrawing a high bid to block honest sellers
(`solodit-guardian-audits-2023-04-08-nftr-0-3`), and — at the
infrastructure level — the Priority Gas Auctions and MEV dynamics
catalogued in `arxiv-2603.07716`, where the gas market itself becomes an
adversarial auction over ordering.

## Variants

### V1: Dutch/GDA price-curve math errors

The price function is the heart of a Dutch auction, and small math
mistakes corrupt every quote. Observed sub-cases:

- **Division-before-multiplication precision loss.** `scalarPrice`
  divides by the time denominator before multiplying by the base price,
  so the result is rounded down further than necessary; multiplications
  should always precede divisions
  (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-1`).
- **Broken elapsed-time logic.** The `elapsedTime` helper returns wrong
  values in the zero-window case, in the boundary case where auction and
  window elapsed times are equal, and while a window is active the
  timestamp argument equals `startTimestamp` so elapsed time is always 0
  — the price is computed from garbage
  (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-2`).
- **Missing lower price bound on the decayed spot price.** In Sudoswap's
  GDACurve the new spot price is written without re-checking it against
  `MIN_PRICE` (the bound is only enforced in `validateSpotPrice`), so
  under high lambda / low demand the price can decay below the intended
  floor (`solodit-cyfrin-2023-06-01-sudoswap-1-2`).

### V2: Bid settlement and refund accounting

Even with a correct curve, the settlement step that converts a bid into
tokens-owed is a rounding minefield:

- **Remainder lost to the bidder.** `reserves -= volume / price` and
  `claim += volume / price` round down; the seller is credited the full
  `volume` while the bidder's claim loses the remainder. Fix: refund the
  division remainder to the bidder
  (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-1`).
- **Round-to-zero with low-decimal tokens.** When `purchaseToken` is
  USDC/USDT/WBTC (6–8 decimals) against an 18-decimal reserve, or when
  `volume < price`, `volume / price` rounds to 0 — the bidder pays in
  full and receives nothing
  (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-1-0`).
- **Charging computed price, not bid amount.** A Dutch-auction bid only
  pulls funds sufficient to cover the *current calculated* price rather
  than the submitted bid amount; legitimate as business logic, but it
  must be explicitly confirmed because the gap is silent
  (`solodit-zokyo-2022-11-16-onemind-3-1`).

### V3: Auction lifecycle and state-machine integrity

- **Unvalidated timestamps.** `createAuction` allowing `endTimestamp ==
  startTimestamp` (zero duration), an end far in the future (never ends),
  or a start far in the future (never starts) can strand reserves and
  bids forever; enforce min/max duration and a max start delay
  (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-0`). A
  related defect: an auction created with `startingOriginPrice == 0`
  leaves `state.price == 0`, defeating the "auction exists" guard and
  allowing re-creation / a double `transferFrom`
  (`...-3-0`).
- **No time gating on bids.** Bids accepted regardless of the configured
  start/end window mean the auction schedule is advisory only
  (`solodit-zokyo-2022-11-16-onemind-2-0`).
- **Non-atomic finalize lets the account close before delivery.** When
  fee payment and `close_auction` can be called as separate
  transactions, all lamports drain and the account closes, after which
  `finalize` reverts and the winner never receives the NFT; merge the
  steps so settlement is atomic (`solodit-zokyo-2022-11-16-onemind-0-0`).
- **No recovery when an auction ends without bids.** Listed tokens get
  locked because the recover function caps recoverable amount at
  `balance - totalAllocation`; a no-bid auction needs an explicit
  reclaim path (`solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-6`).
- **Bidding-window DoS.** A `public` `fulfillWindow` that sets
  `window.processed = true` can be called externally to make every
  subsequent `commitBid` revert until the auction ends, halting all new
  bids; restrict the function and gate completion behind an inactive-auction
  modifier (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-0`).
- **Bootstrap / empty-book reverts.** With no existing bid, an ownership
  lookup on `address(0)` reverts so the very first bid can never be
  placed; bypass the check on an empty book
  (`solodit-guardian-audits-2023-04-08-nftr-0-1`).

### V4: Bid front-running, sniping, and griefing

Auctions live in an adversarial mempool (`swc-114`): pending bids and
reveals are observable, and ordering is for sale.

- **Griefing by bid-then-withdraw / transfer.** An attacker places a bid
  higher than the current best, blocking honest buyers, then withdraws it
  (or transfers the eligibility token) so honest bids are lost and the
  seller can never settle; mitigation is to require several blocks to
  elapse before a bid can be overwritten/withdrawn so the griefer risks
  their funds (`solodit-guardian-audits-2023-04-08-nftr-0-3`).
- **Refund/withdraw eligibility coupled to mutable ownership.** Tying the
  ability to withdraw a bid to current NFT ownership lets a bidder who
  later acquires the asset get stuck unable to reclaim their bid
  (`solodit-guardian-audits-2023-04-08-nftr-1-3`).
- **Unbounded bid expiration.** Missing validation on a bid's
  `expiration` lets already-expired or never-expiring bids enter the book
  and be "updated"; constrain expiration to a sane future window
  (`solodit-pashov-audit-group-2023-02-01-punk-bid-0-1`).
- **Sealed-bid leakage / ordering markets.** "Sealed" bids on a public
  chain are not private unless a commit-reveal hash hides them until
  reveal; otherwise transaction-order dependence (`swc-114`) lets
  observers undercut/outbid. At the infrastructure layer the ordering
  itself is auctioned — Priority Gas Auctions and the broader MEV supply
  chain (`arxiv-2603.07716`) — so any auction whose outcome depends on
  "who got in first" inherits that adversarial dynamic.

### V5: Token-compatibility assumptions

- **Fee-on-transfer / rebasing reserve tokens.** Caching the expected
  transfer amount (`state.reserves = reserveAmount`) breaks when the token
  takes a transfer fee or rebases, leaving the cached accounting out of
  sync with the real balance and stranding or over-crediting tokens;
  measure balance delta or document non-support
  (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-3`).
- **CEI / reentrancy in bid handling.** `commitBid` performing the
  `transferFrom` before completing state updates risks reentrancy
  (especially with ERC777-style hooks); apply `nonReentrant` and move
  the transfer to the end
  (`solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-1`).

## Audit checklist

Price curve & settlement math:
- Are all multiplications performed before divisions in the price and
  settlement formulas to minimize rounding-down loss?
- Does the settlement compute a division remainder (e.g. `volume / price`)
  that is silently lost — and is that remainder refunded to the bidder?
- Can the bidder's computed claim round to zero with low-decimal purchase
  tokens or when `volume < price`?
- Is the decayed/updated spot price re-validated against `MIN_PRICE` (or a
  floor) at the point it is written, not only at configuration time?
- Is the elapsed-time / decay computation correct at the boundaries
  (zero windows, window active, start == now)?

Lifecycle & state machine:
- Are `startTimestamp`/`endTimestamp` validated for min and max duration
  and a bounded start delay, so funds cannot be stranded forever?
- Are bids time-gated to the active auction window?
- Is settlement (asset delivery + fee payment + account close) atomic, so
  the auction account cannot be closed before the winner receives the asset?
- Is there a recovery/reclaim path when an auction ends with no bids?
- Can a `public` window/settlement helper be called externally to DoS all
  future bids (e.g. by flipping a `processed` flag)?
- Can the first bid be placed on an empty book without reverting on a
  zero-address/default lookup?
- Can an auction be (re)created with a zero starting price that defeats an
  "auction exists" guard?

Adversarial ordering & griefing:
- Can a bidder place a high bid and then withdraw/transfer it to grief the
  seller, with no per-block lock before overwrite/withdrawal?
- Is withdraw/refund eligibility decoupled from mutable external state
  (e.g. current NFT ownership)?
- Is bid `expiration` constrained to a sane future window (not already
  expired, not infinite)?
- For "sealed-bid" designs, are bids hidden behind a commit-reveal hash
  rather than stored/visible in calldata or state?
- Does auction outcome depend on raw mempool ordering in a way that is
  exploitable via transaction-order dependence / MEV?

Token & reentrancy:
- Does the auction tolerate fee-on-transfer / rebasing tokens, or is the
  supported token set documented and enforced?
- Does bid handling follow checks-effects-interactions and/or use a
  reentrancy guard around external transfers?

## Prior incidents

- **Treasure DAO (2022-03-03) — ~$1.4M**: The NFT marketplace's `buyItem`
  settlement function failed to validate `_quantity > 0`, so an attacker
  could "buy" listings for zero payment and still receive the NFT — the
  same class of unvalidated-settlement-input failure that auction
  finalize/settlement steps must guard against [cites: `rekt-treasure-dao-rekt`].
- **Rolling Dutch Auction (audit, 2023-03) — caught pre-deployment**:
  Critical bidding-window DoS (anyone could permanently revert new bids)
  and critical division-rounding bidder value loss were both found in
  audit, illustrating V2/V3 in a live Dutch-auction codebase
  [cites: `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-0`,
  `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-1`].
- **Onemind Auction House (audit, 2022-11) — caught pre-deployment**:
  High-severity finding where the auction account could be closed before
  the NFT was transferred to the winner, an atomic-settlement failure
  [cites: `solodit-zokyo-2022-11-16-onemind-0-0`].

## References

- corpus entries:
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-0` — DoS: new bids revert after window expires
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-1` — Division rounding loses bidder value
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-0-2` — Flawed `elapsedTime` price logic
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-1-0` — Low-decimal token bids round to zero
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-0` — Missing timestamp input validation
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-1` — Precision loss in `scalarPrice` (div before mul)
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-3` — Fee-on-transfer / rebasing token mismatch
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-0` — `price == 0` auction can be re-created
  - `solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-3-1` — `commitBid` CEI / reentrancy
  - `solodit-zokyo-2022-11-16-onemind-0-0` — Account closed before NFT delivered to winner
  - `solodit-zokyo-2022-11-16-onemind-2-0` — No time check when bidding
  - `solodit-zokyo-2022-11-16-onemind-3-1` — Calculated price charged, not bid amount
  - `solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-6` — No token recovery when auction ends with no bids
  - `solodit-cyfrin-2023-06-01-sudoswap-1-2` — GDACurve new spot price not bounded by `MIN_PRICE`
  - `solodit-guardian-audits-2023-04-08-nftr-0-1` — First bid reverts on empty book
  - `solodit-guardian-audits-2023-04-08-nftr-0-3` — Griefing sellers via bid-then-withdraw
  - `solodit-guardian-audits-2023-04-08-nftr-1-3` — Withdraw eligibility tied to mutable ownership
  - `solodit-pashov-audit-group-2023-02-01-punk-bid-0-1` — Unconstrained bid expiration
  - `swc-114` — Transaction Order Dependence (front-running / race conditions)
  - `rekt-treasure-dao-rekt` — NFT marketplace settlement missing `_quantity > 0` ($1.4M)
  - `arxiv-2603.07716` — SoK on MEV: Priority Gas Auctions and adversarial ordering markets
