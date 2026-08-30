---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-10
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: User cannot claim dividends after withdrawing their DRVS tokens
vuln_class: []
---

# User cannot claim dividends after withdrawing their DRVS tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In `dividends_claim`, the function checks that `client_community_state.header.drvs_tokens` is greater than zero for the user to be eligible to claim their dividend tokens.

```rust
    if client_community_state.header.drvs_tokens > 0 {
        let clock = Clock::get().map_err(|err| drv_err!(err.into()))?;
        let slot = clock.slot as u32;
        for (d, b) in client_community_state
            .data
            .iter_mut()
            .zip(community_state.base_crncy.iter_mut())
        {
            client_state.resolve(AssetType::Token, b.crncy_token_id, TokenType::Asset, true)?;
            let amount = ((((b.rate - d.dividends_rate)
                * client_community_state.header.drvs_tokens as f64)
                as i64)
                + d.dividends_value)
                .min(b.funds)
                .max(0);
            client_state.add_asset_tokens(amount)?;
            b.funds -= amount;
            d.dividends_rate = b.rate;
            d.dividends_value = 0;
            solana_program::log::sol_log_data(&[bytemuck::bytes_of::<EarningsReport>(
                &EarningsReport {
                    tag: log_type::EARNINGS,
                    client_id: client_state.id,
                    amount,
                    token_id: b.crncy_token_id,
                    time: clock.unix_timestamp as u32,
                    ..EarningsReport::zeroed()
                },
            )]);
        }
        client_state.header.try_upgrade()?.slot = slot;
    }
```
Our current design allows a user to withdraw their DRVS tokens without claiming dividends. This means that if the user sells their tokens after withdrawing, they will not be able to claim dividends until they deposit some DRVS tokens again.

**Impact:** User will not be able to claim their `dividends_value` even if it is greater than zero, unless their DRVS deposit is also greater than zero.


**Recommended Mitigation:** Allow claiming the dividend value even when `client_community_state.header.drvs_tokens` is zero.

**Deriverse:** Fixed in commit [4dba9d](https://github.com/deriverse/protocol-v1/commit/4dba9dcc728fc78594f75aea086431b385fcb6f3).

**Cyfrin:** Verified.
