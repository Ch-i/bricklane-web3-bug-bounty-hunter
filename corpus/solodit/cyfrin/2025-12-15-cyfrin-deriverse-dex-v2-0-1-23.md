---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-23
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: '`perp_statistics_reset` can be used by users to skip `collactable-losses`
  while selling market seat'
vuln_class: []
---

# `perp_statistics_reset` can be used by users to skip `collactable-losses` while selling market seat

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Inside `perp-statistics-reset` we set [soc loss funds](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/processor/perp_statistics_reset.rs#L91) to zero without checking if user incurred losses.
```rust
//inside perp-statistics-reset
    client_state.perp_info4()?.soc_loss_funds = 0;
```
if user would have incurred losses, these funds would be positive which means, this is the amount of funds protocol should collect and add to insurance funds at the time when user sells the market seat. we set those to 0 and later call `check-soc-loss` which in turn would make this funds -ve. If now user calls `sell-market-seat` he gets back this funds and [insurance funds](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/processor/sell_market_seat.rs#L123) are also reduced by this amount which is incorrect.
```rust
//inside sell-market-seat
    let collactable_losses = info.funds().min(client_state.perp_info4()?.soc_loss_funds);
    engine.state.header.perp_insurance_fund += collactable_losses;

    client_state.add_crncy_tokens((info.funds() - collactable_losses).max(0))?;

```
if user has incurred losses earlier & his `soc-loss-funds` is positive, he should not be allowed to use `perp-statistics-reset`, he can simply use it to wipe "the amount he owns to protocol on exiting the position".

**Impact:** Users can missuse this to clean their soc loss records which store how much they owe to protocol.

**Recommended Mitigation:** Get user's soc losses, if they are positive, which means user owes the amount to protocol, avoid statistics resetting and revert.

**Deriverse:** Fixed in commit: [e5af702](https://github.com/deriverse/protocol-v1/commit/e5af70204e812ed9f388a0dea23ff89fd15f2394)

**Cyfrin:** Verified.
