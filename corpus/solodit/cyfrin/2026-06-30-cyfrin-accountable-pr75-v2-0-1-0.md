---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::settle, refund` leave escrow stuck when the strategy is stale
  or paused and `_refundable` recognizes neither, permanently inflating `unsettledEscrow`'
vuln_class: []
---

# `DepositGateway::settle, refund` leave escrow stuck when the strategy is stale or paused and `_refundable` recognizes neither, permanently inflating `unsettledEscrow`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** When the strategy is NAV-stale or paused, the deposit settlement path has no exit for an otherwise-deliverable request. `DepositGateway::settle` (`src/modules/DepositGateway.sol:163-192`) calls `IAccountableVault::deposit`, which routes through `AccountableYield::onDeposit` (`src/strategies/AccountableYield.sol:405-412`). That hook carries both `whenNotStale` and `whenNotPaused`, so it reverts while the NAV grace period has expired or the strategy is paused. The settle loop swallows that revert in its `try/catch` and simply leaves the request pending. The natural escape - `refund` - does not help: `_refundable` (`src/modules/DepositGateway.sol:280-302`) enumerates loan-state, gateway-mismatch, capacity, KYC, Whitelist, and lowered-`minDeposit` branches, but treats neither stale NAV nor pause as refundable, so `refund` reverts `NotRefundable`. The request is therefore neither settleable nor refundable for the duration of the stale/paused window.

**Files:**

- `DepositGateway::settle, refund` (`src/modules/DepositGateway.sol`)
- `DepositGateway::_refundable` (`src/modules/DepositGateway.sol`)
- `AccountableYield::onDeposit` (`src/strategies/AccountableYield.sol`)

**Impact:** A whitelisted, correctly-sized request that should settle cannot settle and cannot be refunded while the strategy is stale or paused. Because the request stays pending, its escrow remains summed into `unsettledEscrow`, which `requestDeposit` uses as the capacity reservation (`assets + unsettledEscrow > maxAssets`). The stuck escrow throttles available headroom for every other depositor until a new NAV is published or the strategy is unpaused. The condition is transient and self-resolves once the strategy returns to a fresh, unpaused state, so funds are recoverable rather than lost.

**Recommended Mitigation:** Add a refundable branch for the stale/paused condition so a depositor can recover escrow when settlement is blocked by strategy state rather than by their own eligibility. Either expose the strategy's stale/paused state to `_refundable` and return `true` when settlement is blocked by it, or allow the depositor to cancel a Passed-epoch request back to themselves under that condition. Preserve the existing branches so eligibility-based refunds continue to work.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** This leaves a minor griefing vector open where anyone could refund someone while the vault is paused, even if the user would want to wait and join once it's unpaused. They'd then have to wait yet another nav update

**Accountable:** Fixed in commit [`2b60b00`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/2b60b0008853a791ae52354b455ae3894eb1ef8d)

**Cyfrin:** Verified.
