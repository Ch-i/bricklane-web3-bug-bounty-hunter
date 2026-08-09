---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::requestDeposit` capacity reservation lets one requester exhaust
  headroom and block all other depositors'
vuln_class: []
---

# `DepositGateway::requestDeposit` capacity reservation lets one requester exhaust headroom and block all other depositors

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `DepositGateway::requestDeposit` (`src/modules/DepositGateway.sol:84-110`) reverts `ExceedsMaxDeposit` when `assets + unsettledEscrow > maxAssets`, reserving capacity against the running `unsettledEscrow`. An actor can size a single request to consume all remaining headroom, after which every other `requestDeposit` reverts for lack of capacity. While the epoch is still Open, the actor then calls `cancelDeposit` (`src/modules/DepositGateway.sol:113-132`), which returns their full escrow and decrements `unsettledEscrow`. The sequence is self-reversing: the griefer recovers their funds while having blocked others for the interval.

**Files:**

- `DepositGateway::requestDeposit, cancelDeposit` (`src/modules/DepositGateway.sol`)

**Impact:** A single actor can repeatedly deny other users the ability to subscribe to an epoch at near-zero net cost, since the blocking escrow is fully recoverable via cancel. This is a repeatable, self-reversing denial of service against other subscriptions, gated by the available capacity headroom. No funds are lost - the griefer's escrow returns to them and victims keep their tokens - but legitimate depositors are denied entry while the headroom is held; the condition is fully recoverable once the griefer cancels or the epoch advances.

**Recommended Mitigation:** Remove the cost-free cancellation that makes the reserve-then-recover loop repeatable, and treat a deposit request as a firm commitment that settles at the next NAV rather than escrow the requester can reclaim on demand. Without a free cancel, reserving the remaining headroom requires committing capital that is actually deposited and minted into shares at settlement, so an actor can no longer hold and release shared capacity at will to deny other subscriptions: blocking an epoch would cost a real, non-recoverable deposit per epoch instead of being free and repeatable. If preventing a single committed deposit from occupying an epoch's entire headroom is also a concern, additionally impose a per-account capacity limit within an epoch so no single request can monopolize the shared headroom.

**Accountable:** Fixed in commit [`22bf5d5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/22bf5d58fc104094375b82ac7e39aac3ce6dd12b)

**Cyfrin:** Verified.
