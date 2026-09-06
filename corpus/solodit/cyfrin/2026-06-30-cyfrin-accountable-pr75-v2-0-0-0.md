---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::settle` prices escrowed deposits at the live share price,
  not the epoch''s closing NAV'
vuln_class: []
---

# `DepositGateway::settle` prices escrowed deposits at the live share price, not the epoch's closing NAV

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** The gateway batches deposits into epochs so they "enter `AccountableYield` only at the post-NAV price" (`DepositGateway` contract NatSpec, `src/modules/DepositGateway.sol:19`). However, `_passEpoch` records only a timestamp into `epoch.navMeasuredAt` (`src/modules/DepositGateway.sol:271,276`) and never stores a share price. `settle` is permissionless, requires only `epoch.status == Passed` (`src/modules/DepositGateway.sol:166`), and mints by calling `IAccountableVault(vault).deposit(...)` (`src/modules/DepositGateway.sol:175`), which routes to `AccountableYield::onDeposit` and prices at the LIVE `_sharePrice(share)` computed at the settle block (`src/strategies/AccountableYield.sol:423,617-623`). `settle` has no deadline and `cancelDeposit` reverts once the epoch is past `Open` (`src/modules/DepositGateway.sol:121`). So the price a depositor realizes is whatever the live price is when their request is settled, not the NAV that closed their epoch.

The protocol mitigates this operationally: a keeper bot settles each passed epoch promptly after the NAV update that closed it, so under normal operation depositors are settled at approximately the closing NAV. The residual is the window between an epoch passing and the keeper settling it. Because NAV updates are not on a fixed schedule and `settle` has no on-chain time bound, if a later `publishRate` lands before the keeper settles a request (keeper lag, downtime, or two NAV updates close together), the still-unsettled depositor can settle into the newer price. `settle` is also paginated for large epochs, so requests in a big batch stay unsettled across several blocks. Continuous management-fee accrual additionally means even a prompt settle lands slightly below the closing price.

**Files:**

- `DepositGateway::settle, _passEpoch` (`src/modules/DepositGateway.sol:163-219,269-277`)
- `AccountableYield::onDeposit, _sharePrice` (`src/strategies/AccountableYield.sol:405-427,617-623`)

**Impact:** When a depositor settles at a price below their epoch's closing NAV, they mint more shares than their deposit warrants, and the excess is diluted away from existing vault shareholders - not from the keeper operator or the protocol. The likelihood is materially reduced by the keeper bot, but the exploit is bounded by keeper uptime and NAV-update spacing rather than by code: a stale passed epoch remains settleable at an arbitrarily later price until someone settles it, so the worst-case window is unbounded and the loss falls on passive LPs who have no involvement in the keeper.

The same defect also lets a keeper discriminate between depositors in a single epoch. `settle` is permissionless, takes a caller-supplied `requestIds` subset, and mints at the live price (`src/modules/DepositGateway.sol:163,168-170`), so the keeper chooses both which requests to settle and in which block. It can settle a favored cohort while the price is low and defer the rest to a higher-priced block, leaving co-epoch depositors who expected one price with different share amounts. The frozen-price mitigation below closes this too: every request in an epoch would settle against the same snapshot.

**Recommended Mitigation:** Add an on-chain staleness guard so the keeper is the happy path and the contract is the backstop: in `settle`, once `strategy.lastNavMeasuredAt()` has advanced past the epoch's `navMeasuredAt`, reject the settle and route the request to `refund` / re-request instead of minting at the newer live price. When the keeper settles before the next NAV update the guard never triggers and behavior is unchanged; when the keeper misses, the request is refunded rather than settled at an exploitable price. This preserves the simple live-pricing design while bounding the residual to a refund rather than LP dilution. Alternatively, snapshot the share price at `_passEpoch` and mint against that frozen value in `settle`.

**Accountable:** Fixed in commit [`22bf5d5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/22bf5d58fc104094375b82ac7e39aac3ce6dd12b)

**Cyfrin:** Verified. `settle` invalidates the epoch (`EpochStatus.Invalid`) if a newer NAV landed after close; those requests must refund, not mint at the new price.
