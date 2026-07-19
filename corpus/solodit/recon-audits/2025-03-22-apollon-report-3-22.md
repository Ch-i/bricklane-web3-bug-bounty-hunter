---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-22
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-23] Analysis - Some thoughts, consideration and advice for next steps'
vuln_class: []
---

# [L-23] Analysis - Some thoughts, consideration and advice for next steps

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

Logically you can chunk the code into 3 components

- Feeds
- Swap and Stake Operations
- Core

-----

It may be best to write fuzz and invariant tests on these separately and then you can consider adding a new 

**Generic Gas Advice**

**Use Immutables**

The codebase relies on caching storage values into memory to reduce SLOADs

You could also deterministically deploy each contract (since contract addresses are derived from address + nonce) and set those up as immutable variables



**Alex's Review Status**

- [x] AlternativePriceFeed
- [x] BorrowerOperations
- [x] CollSurplusPool
- [X] DebtToken*
- [X] HintHelpers*
- [x] LiquidationOperations
- [x] PriceFeed
- [x] RedemptionOperations
- [x] ReservePool
- [x] SortedTroves
- [x] StabilityPool
- [x] StabilityPoolManager
- [x] StakingOperations
- [x] StoragePool
- [x] SwapERC20
- [X] SwapOperations
- [x] SwapPair
- [x] TokenManager
- [X] TroveManager

**Breaking CEI**

CEI stands for `Check Effects Interactions` which ensures that no state changing operations are done after external calls that the system may rely on

Transferring collateral before updating internals should be considered as highly risky, not just in lack of `nonReentrant` guards but in general due to the system reliance on cross contract operations

In my opinion all CEI concerns should be addressed, unless you can ensure that no token will ever have hooks

But in general, solving CEI even in those cases is a better choice as it will save time from auditors looking into those concerns and will ensure that the system is safe even if a token with hooks were to be introduced

**Price Staleness**

Relative staleness is imo not a valid idea, all prices must be validated and trove status must be checked against the latest available prices

In lack of that, a Trove could end up generating bad debt due to having it's CR computed with stale prices


**Alternative Price Feed**

Fundamentally it hardcodes prices, offers a guarantee for staleness

No guarantee for deviation threshold (how accurate, and how fast it will react to sudden price changes)

An hardcoded price should be viewed as a massive liability and risk, it's a fundamental issue for developers as well as for end users

It may be best to have 2 prices:
- A borrow price 
- A liquidation price

Fundamentally making the assets:
- Less valuable for borrowing (So you can borrow less)
- Overpriced for liquidations (so liquidations happen faster)


**StakingOperations**

This contract is effectively a Masterchef and can be reviewed fairly independently

Race conditions around interactions with the pool are pretty delicate

Beside that, the code is separated so this contract can be re-reviewed independently

**SwapPair**

Fundamentally there are ways to sidestep the intended `_requireCallerIsOperations` via direct transfer + sync

The added fee is the most delicate aspect and I believe tighter checks to ensure that only an intended amount is paid should be added

The x * y = k formula is highly capital inefficient in this case but that's not something easily fixable

I think the way `_getDexPrice` is calculate is a bit naive as this is not a price but rather the ratio of reserves any purchase will incur an additional price impact that is not accounted there, additionally taking the average of the before and after makes it so that some swaps that push the price out of the oracle price do not pay a sufficiently high fee


**SwapOperations**

- Donation to force a ratio
- Fee math / Path Math

**TokenManager**

Fundamentally some small risks tied to token config

The biggest risk is tied to changing risk config params

**CollSurplusPool**

The observations around `CollSurplusPool` are:
- Double loop vs mapping, this is generally a pattern you should avoid
- Breaking CEI - you should consider CEI a key part of your security posture, breaking CEI should not be underestimated as a "basic mistake"

**StoragePool**

The main risks around `storagePool` are tied to a desynchronization between the value that it tracks, and the values being tracked in other contracts, such as `TroveManager`

I believe invariant testing should be added to ensure that these values are synchronized at all times 

**DebtToken**

Fundamentally just tracks the debt and is also used as a scaling factor for oracle

I believe that the logic for Stock Splits can be massively simplified by hardcoding the divisor and the dividend, with no particular change in risk profile

**HintHelpers**

The main risk I see is how the SortedTroves uses cached values, but HH is using live values

The discrepancy may be used to trigger Recovery Mode via Redemptions

**SortedTroves**

The main changes are tied to how data is stored as well as the removal of insert / remove, in favour of an update function

The sorting is done via cached CR, but that's not a distinctive change as ultimately even Liquidity is just sorting based on a CR value that is accepted at face value

This seems to be a good candidate for differential fuzzing to compare the two implementations

To be honest I'm not sure why the implementation was changed as this ultimately behaves very similarly

**Swap Operations**

The main risks are tied to manipulating the debt being taken by users, as well as possible race conditions
For these operations, oracle staleness is also an important factor

I believe these contracts can be mostly reviewed separately in the future as they feel pretty separated

If you can end up separating the debts math from swaps, I think these contracts can be fully separated long term

**StabilityPool**

CEI concerns, code is fairly complex but is pretty much the same logic as in Liquity

**Stability Pool Manager**

Fundamentally tracks accounting, for liquidation, which looks fine

The main aspect that I'm not fully convinced by is the usage of the Reserve Pool, which seems not be taken into account by the LiquidationOperations

**Redemption Operations**

Round downs seem to be in favour of the protocol which doesn't seem to create a risk

Due to the fact that Troves are sorted by cached CRs, some Troves "in the middle" may be underwater, meaning that redeeming them will revert, this will cause reverts but it shouldn't cause major issues as you could simply perform a redemption, then another one, etc..



**Recommended Next Steps**

I recommend spending quite some time into the economic and technical implications that come with:
- Oracle staleness
- Redemptions, Liquidations and Swap Fees

I also recommend adding a few invariant tests for system wide invariants that would guarantee:
- Intended execution
- Inability to attack the system (self-liquidations, triggering RM)
- Ability to execute operations when they are necessary (e.g. liquidations)

Some suggested invariants are listed here:
https://github.com/GalloDaSballo/Apollon-Review/issues/44
