---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::forcePassEpoch` is permissionless and can strip a pending
  depositor''s cancel window'
vuln_class: []
---

# `DepositGateway::forcePassEpoch` is permissionless and can strip a pending depositor's cancel window

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `DepositGateway::forcePassEpoch` (`src/modules/DepositGateway.sol:147-160`) is permissionless and succeeds as soon as `strategy.lastNavMeasuredAt()` exceeds the epoch's `openNavMeasuredAt`. A pending deposit can be cancelled only while its epoch is Open: `cancelDeposit` (`src/modules/DepositGateway.sol:113-132`) reverts `EpochNotOpen` once the epoch leaves `EpochStatus.Open`.

In the normal flow a NAV publish closes the epoch atomically: `publishRate` calls `onNavUpdate`, which passes the epoch in the same transaction, so the cancel window closes with the publish itself and no Open epoch remains for `forcePassEpoch` to act on. The distinct case `forcePassEpoch` targets is a missed notification: `publishRate` wraps `onNavUpdate` in a `try/catch` (`GatewayNavUpdateFailed`), so if that notify reverts, `lastNavMeasuredAt` advances while the epoch stays Open. In that window a third party can call `forcePassEpoch` to move the epoch from Open to Passed, locking in every pending request at the already-published NAV before its depositor has a chance to cancel.

**Files:**

- `DepositGateway::forcePassEpoch` (`src/modules/DepositGateway.sol`)
- `DepositGateway::cancelDeposit` (`src/modules/DepositGateway.sol`)

**Impact:** A depositor who would have cancelled after an adverse NAV publish can be front-run out of their cancel window by anyone calling `forcePassEpoch` in the same block or shortly after. The request then settles at the post-publish NAV rather than being refundable on demand. The depositor still receives shares at the published price, so this is a loss of optionality (the ability to back out at the last moment) rather than a loss of principal; the user does not gain the right to cancel back after Passed.

**Recommended Mitigation:** Treat a deposit request as a firm commitment and remove the cancellation path entirely, so there is no last-moment cancel window for a force-pass to strip. The depositor is then priced at the next NAV regardless of who triggers the pass or when, exactly the trade-off a direct vault deposit already makes, and exits afterward through the strategy's normal (async) withdrawal path if the resulting price is unfavorable. With no cancel path, the timing and permissionlessness of `forcePassEpoch` no longer affect the depositor's outcome.

**Accountable:** Fixed in commit [`22bf5d5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/22bf5d58fc104094375b82ac7e39aac3ce6dd12b)

**Cyfrin:** Verified.
