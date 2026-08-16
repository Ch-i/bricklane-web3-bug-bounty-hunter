---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::requestDeposit` minDeposit gate is weaker than the vault''s
  `MIN_AMOUNT_WEI` floor, leaving sub-floor requests permanently unsettleable and
  non-refundable'
vuln_class: []
---

# `DepositGateway::requestDeposit` minDeposit gate is weaker than the vault's `MIN_AMOUNT_WEI` floor, leaving sub-floor requests permanently unsettleable and non-refundable

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `DepositGateway::requestDeposit` (`src/modules/DepositGateway.sol:84-110`) enforces `assets >= loan.minDeposit` but does not enforce the vault's own minimum-amount floor (`MIN_AMOUNT_WEI`, 10_000) that `IAccountableVault::deposit` checks at settle time. If the manager sets `loan.minDeposit` below that floor, a request escrowed at an amount between the two (e.g. `minDeposit <= assets < MIN_AMOUNT_WEI`) is accepted, but at settle the vault's minimum-amount check reverts and the `try/catch` in `settle` (`src/modules/DepositGateway.sol:163-192`) swallows it. The request is then not refundable either: `_refundable`'s lowered-`minDeposit` branch (`src/modules/DepositGateway.sol:280-302`) tests `strategy_.loan().minDeposit > assets`, which is false for a request at or above `minDeposit`, and no other branch matches a sub-floor amount.

The same floor gap also admits zero-asset requests at its lower extreme. With `minDeposit` configured as zero, `assets == 0` satisfies `assets >= minDeposit`, and because `safeTransferFrom` moves no tokens the request costs only gas. A submitter can then create an unbounded number of zero-asset requests, each likewise unsettleable (the vault rejects the zero amount) and unrefundable, each pinning `pendingCount` above zero so the epoch can never finalize. The zero-asset variant escrows nothing, so its harm is settlement griefing and keeper-gas inflation rather than stranded funds, but it stems from the same missing floor check.

**Files:**

- `DepositGateway::requestDeposit` (`src/modules/DepositGateway.sol`)
- `DepositGateway::_refundable` (`src/modules/DepositGateway.sol`)

**Impact:** A request sized between the gateway's `minDeposit` and the vault's hard minimum can be permanently stuck: it cannot settle (vault rejects sub-floor amounts) and cannot be refunded (`_refundable` returns false for it). The escrow stays summed into `unsettledEscrow`, and because the request keeps `pendingCount` above zero, its epoch never finalizes. The depositor cannot recover the escrowed amount through the contract's own paths; recovery would require a manual intervention outside the defined flow. Triggering it requires the manager to have configured `minDeposit` below the vault floor.

**Recommended Mitigation:** Enforce the vault's minimum-amount floor at request time so the gateway never accepts an amount the vault will later reject - either validate `assets >= MIN_AMOUNT_WEI` in `requestDeposit` alongside the `minDeposit` check, or constrain `setTerms`/`updateTerms` so `minDeposit` can never be set below the vault floor. Additionally, add a `_refundable` branch covering amounts the vault would reject so any stranded request retains a refund path.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
