---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Withdrawals priced at execution problematic during large price swings
vuln_class: []
---

# Withdrawals priced at execution problematic during large price swings

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** Withdrawals are “price-locked” at request time: `requestRedeem` stores `shares` and the computed `assetsAfterFee = previewRedeem(shares)` using the at-request exchange rate. When an agent later calls `processWithdrawal`, the vault burns the escrowed `shares` but pays out the stored asset amount, not what those shares are worth at execution.

**Impact:** If the share price has fallen in the interim (e.g., oracle update, Core PnL loss, depeg), early requesters are effectively overpaid relative to the current price, with the shortfall socialized to remaining shareholders. In extreme drawdowns this can accelerate bank-run dynamics and drain the vault faster than intended possibly to the point of insolvency.

**Recommended Mitigation:** Consider using price at execution. Store only `shares` at request time and compute `assetsAfterFee` at processing using the current exchange rate (i.e., `previewRedeem(shares)` then). Possibly with execution guardrails with acceptable slippage bounds (protocol default and/or user-provided).

**Button:** Fixed in commit [`9cde24c`](https://github.com/buttonxyz/button-protocol/commit/9cde24caa4b3f5f37a059bb2fde172cfa374d3a9) by moving to pricing at execution.

**Cyfrin:** Verified. Price now taken at execution.
