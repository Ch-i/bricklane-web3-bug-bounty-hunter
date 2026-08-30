---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-19
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Users can sell their market seat without paying loss coverage
vuln_class: []
---

# Users can sell their market seat without paying loss coverage

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** When users incur loss, its covered from available insurance funds and is stored and tracked inside `taker_info4.loss_coverage`, this is what user owes to protocol before he closes his position, because insurance funds have been used to cover up for these losses incurred by user. Inside `sell-market-seat` we are calling [close_account](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/program/processor/sell_market_seat.rs#L127), it does not check for users's loss coverage, it only checks
```rust
            if (*self.perp_info3).bids_entry != NULL_ORDER
                || (*self.perp_info3).asks_entry != NULL_ORDER
                || self.current_instr_index >= self.assets.len()
            {
                bail!(ClientDataDestruction);
            }
```
if user has incurred losses in past and insurance funds covered this loss, he must pay back these funds before closing the seat, the function [`try_to_close_perp`](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/state/client_primary.rs#L701) checks this properly, if user has pending loss coverage we subtract it from users' funds, this way he pays back his losses and then closes the position.
```rust
            if (*self.perp_info4).loss_coverage > 0 {
                let delta = (*self.perp_info4)
                    .loss_coverage
                    .min((*self.perp_info).funds);
                if delta > 0 {
                    engine.state.header.perp_insurance_fund += delta;
                    (*self.perp_info4).loss_coverage -= delta;
                    (*self.perp_info).funds -= delta;
                }
            }
```

**Impact:** Users can close their seats without paying for their incured losses

**Recommended Mitigation:** Call `try_to_close_perp` instead of `close_perp` inside `sell-market-seat`.

**Deriverse:** Fixed in commit: [e5af702](https://github.com/deriverse/protocol-v1/commit/e5af70204e812ed9f388a0dea23ff89fd15f2394)

**Cyfrin:** Verified.
