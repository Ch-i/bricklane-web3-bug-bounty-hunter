---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Mint match buyers can pay more than `fillAmount` in notional plus fee, guaranteeing
  negative EV
vuln_class: []
---

# Mint match buyers can pay more than `fillAmount` in notional plus fee, guaranteeing negative EV

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** In `MyriadCTFExchange::_settleMintMatch`, two buy orders for opposite outcomes are matched: we compute each side’s notional from their price and the fill size, add the protocol fee, and pull `makerNotional + makerFee` from the maker and `takerNotional + takerFee` from the taker. Each buyer receives `fillAmount` outcome tokens. The maximum value they can ever realize from those tokens is `fillAmount` (one unit of collateral per share at resolution, or market sell at or below that). We do not cap the sum of cost and fee per trader. As a result, when `notional + fee` for a given trader is greater than `fillAmount`, that trader pays more than they can ever recover guaranteeing negative expected value.

This can happen because of changes in fee tiers (e.g. high taker fee at the chosen price bucket). The order struct today has `minFillAmount` for minimum fill size but no upper bound on total cost the signer is willing to pay. So a user can sign an order that, when matched at a given `fillAmount` and fee schedule, charges them more than `fillAmount` with no way to reject that fill on-chain.

**Impact:** A mint-match participant can be filled at a cost-plus-fee that exceeds the maximum redeemable value of the shares they receive, locking in a loss.

**Recommended Mitigation:** Allow users to specify the maximum amount of cost (fee included) they are willing to pay for a fill. For example, add a field to the order (e.g. `maxCostPlusFee`; 0 could mean “no cap” for backward compatibility) and include it in the order hash. Then when settling orders, before pulling collateral from each trader, require that `makerNotional + makerFee <= maker.maxCostPlusFee` (when non-zero) and similarly for the taker. This gives the same kind of protection that `minFillAmount` gives for fill size, but for total cost.

**Myriad:** Acknowledged. We will add application-level warnings to prevent accidental submissions while preserving user autonomy
