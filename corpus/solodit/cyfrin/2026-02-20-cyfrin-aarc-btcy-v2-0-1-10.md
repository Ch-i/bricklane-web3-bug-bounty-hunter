---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-10
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Decimals mismatch risk for supported collateral can cause catastrophic over-mints
vuln_class: []
---

# Decimals mismatch risk for supported collateral can cause catastrophic over-mints

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** The conversion logic in `IBTCYHub` assumes input amounts are expressed in an 8-decimal “BTC base unit”, as reflected by the fixed scaling in both `IBTCYHub::_getMintAmountForPrice` and `IBTCYHub::_getRedemptionAmountForRwa`. If an 18-decimal collateral such as [tBTC](https://etherscan.io/token/0x18084fba666a33d37592fa2633fd49a74dd93a88) is supported and raw token units are mistakenly used (or any offchain pipeline fails to downscale 18→8 before calling the Hub), the calculations will treat 18-decimal units as 8-decimal units.

**Impact:** An 18→8 decimal mis-scaling can cause incorrect minting and redemption settlement by approximately `10^(18-8) = 1e10` for the same human-denominated collateral amount, leading to severe over-issuance and/or incorrect payout amounts from a single operational error.

**Recommended Mitigation:** Add onchain sanity bounds to prevent catastrophic mis-scaling, such as:

* a configurable maximum per-subscription “BTC base unit” amount (expected 8-decimal normalized input), and/or
* a configurable maximum iBTCY mint amount per request/batch,
  chosen to accommodate normal operational sizes while rejecting obviously mis-scaled inputs. This provides defense-in-depth without requiring the Hub to know the underlying collateral token decimals.

Additionally, explicitly state in the function/interface documentation that all subscription/redemption amount parameters are expected to be provided in 8-decimal BTC base units even if the collateral token is 18 decimal.

**Aarc:** Fixed in [`3ffa5a4`](https://github.com/aarc-xyz/btcy-contracts-main/commit/3ffa5a47a059787244bb787a1123c11cf69f3116).

**Cyfrin:** Verified. A max amount for both subscriptions and redemptions is now enforced.
