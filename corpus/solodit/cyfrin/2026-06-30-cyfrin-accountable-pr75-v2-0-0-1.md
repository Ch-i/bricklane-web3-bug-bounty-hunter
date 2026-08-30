---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::cancelDeposit` is a costless NAV-direction option that lets
  a depositor front-run `AccountableYield::publishRate` to avoid unfavorable pricing'
vuln_class: []
---

# `DepositGateway::cancelDeposit` is a costless NAV-direction option that lets a depositor front-run `AccountableYield::publishRate` to avoid unfavorable pricing

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** The gateway's stated purpose is to "batch subscriptions into epochs so deposits enter `AccountableYield` only at the post-NAV price" (NatSpec at `src/modules/DepositGateway.sol:19`): a depositor must commit capital before the NAV that prices them is known, so they cannot cherry-pick a favorable price. That commitment is not enforced. An Open-epoch request can be cancelled, for free, at any time while the epoch is Open: `cancelDeposit` requires only `epoch.status == EpochStatus.Open`, returns 100% of the escrow with no fee, penalty, or cooldown, and credits it to the request owner (`src/modules/DepositGateway.sol:113-132`). The epoch only closes when `publishRate` runs `onNavUpdate` (`src/strategies/AccountableYield.sol:239-245`), and `publishRate(newDeployedValue, measuredAt)` is a single, observable transaction whose `newDeployedValue` argument fully determines the resulting share price - it overwrites `deployedAssets` directly (`src/strategies/AccountableYield.sol:218-220`), and the price is `totalAssets / totalSupply`.

A depositor holding an Open-epoch request can therefore read the pending `publishRate` calldata in the mempool, compute the post-NAV share price, and act one-sidedly: leave the request standing when the move is favorable (NAV down implies a lower price implies more shares per asset), or front-run the publish with `cancelDeposit` and recover the full escrow when the move is unfavorable (NAV up implies a higher price implies fewer shares per asset). The cancel-cancel window ends only at the atomic pricing event, so the depositor always exits before being priced against. This is a one-sided directional option on the strategy NAV, written by the protocol to every Open-epoch depositor at zero premium - the precise behavior the batch-at-post-NAV design exists to prevent. The contract should not let a request be cancelled cost-free across the pricing boundary; the absence of that commitment cutoff is the bug, not a flaw in any present mechanism.

**Files:**

`DepositGateway::cancelDeposit, requestDeposit` (`src/modules/DepositGateway.sol:113-132`, `src/modules/DepositGateway.sol:84-110`); `AccountableYield::publishRate` (`src/strategies/AccountableYield.sol:211-246`)

**Impact:** Existing vault shareholders are diluted. Depositors enter only on NAV declines - minting shares at a cheaper-than-fair price right at a down-NAV print, value that should accrue to existing holders - and abort cost-free on NAV gains. The "post-NAV price" guarantee the gateway exists to provide is defeated and the batching restriction is reduced to cosmetic. The magnitude per cycle is the share-price move the depositor selectively captures, repeatable every NAV cycle; it is bounded by NAV volatility between epoch open and the pricing publish, so the per-event extraction is not parameter-grounded to a fixed figure, but the option is risk-free (the only cost is the cancel gas) and persistent across every cycle.

**Proof of Concept:**
1. The manager has wired the gateway (`setDepositGateway`) and the loan is `OngoingDynamic`. Eve calls `requestDeposit(100_000e6)`; the request joins the current Open epoch E at price P0 = 1.00. Her escrow is fully refundable via `cancelDeposit` for as long as E is Open. Cost so far: gas only.
2. The `dvnPublisher` broadcasts `publishRate(newDeployedValue, measuredAt)`. The transaction sits in the mempool with its calldata visible.
3. Eve computes the resulting share price from `newDeployedValue` (it overwrites `deployedAssets`, driving `_sharePrice`).
4. If the price would rise to 1.05, the deposit would mint Eve ~95_238 shares instead of the 100_000 at P0 - unfavorable. Eve submits `cancelDeposit(requestId)` with a higher priority fee, front-running the publish. The epoch is still Open, so the cancel succeeds and all escrow is returned; the publish prices nothing for her.
5. If instead the price would fall to 0.95, Eve does nothing. The epoch passes and her request later settles minting ~105_263 shares - she captured the loss-driven discount on freshly minted shares, value transferred from incumbent holders.

Repeating each NAV cycle, Eve only ever takes the favorable side, at zero premium. The third-party griefing direction (cancelling someone else's request) is blocked by the `req.user != msg.sender` check at `src/modules/DepositGateway.sol:116`, so only the self-benefit direction applies.

**Recommended Mitigation:** Remove `cancelDeposit` entirely and treat a deposit request as a firm commitment: the depositor is priced at the next NAV and, if that price is unfavorable, exits afterward through the strategy's normal (async) withdrawal path, exactly the trade-off a direct vault deposit already makes.

Because removing cancellation eliminates the only open-epoch exit, pair it with an escape hatch for an open epoch that is never priced (for example a timeout-gated cancel or refund): with cancellation removed and no NAV update, neither `forcePassEpoch` nor `refund` can release open-epoch escrow, so a stalled `publishRate` would otherwise lock a depositor's principal indefinitely. Escrow must continue to route only to the request owner.

**Accountable:** Fixed in commit [`22bf5d5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/22bf5d58fc104094375b82ac7e39aac3ce6dd12b)

**Cyfrin:** Verified. Cancel split into `requestCancelDeposit` + `approveCancelDeposit` (`onlyManager`), gated by `acceptingCancellations` (default `false`).
