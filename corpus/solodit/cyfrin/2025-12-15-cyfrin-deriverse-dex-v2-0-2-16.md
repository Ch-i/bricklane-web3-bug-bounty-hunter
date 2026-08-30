---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-16
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Incorrect Amount Logged in `PerpWithdrawReport`
vuln_class: []
---

# Incorrect Amount Logged in `PerpWithdrawReport`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `perp_withdraw` function logs the requested amount (`data.amount`) instead of the actual withdrawn amount (`amount`) in the `PerpWithdrawReport` event. This creates a discrepancy between the logged amount and the actual funds transferred, particularly when `data.amount == 0` (withdraw all available funds) or when margin call restrictions apply.

In the `perp_withdraw` function, the actual withdrawal amount is calculated based on various conditions:
```rust
let amount = if margin_call {
    let margin_call_funds =
        funds.min(engine.get_avail_funds(client_state.temp_client_id, true)?);
    if margin_call_funds <= 0 {
        bail!(ImpossibleToWithdrawFundsDuringMarginCall);
    }
    if data.amount == 0 {
        margin_call_funds  // Actual amount may differ from data.amount
    } else {
        // ... validation logic ...
        data.amount
    }
} else if data.amount == 0 {
    funds  // Actual amount may differ from data.amount
} else {
    // ... validation logic ...
    data.amount
};
```

The actual funds are transferred using the calculated `amount` variable :

```rust
client_state.add_crncy_tokens(amount)?;
client_state
    .perp_info()?
    .sub_funds(amount)
    .map_err(|err| drv_err!(err))?;
```

However, the log entry records `data.amount` instead of the actual `amount`:

```rust
solana_program::log::sol_log_data(&[bytemuck::bytes_of::<PerpWithdrawReport>(
    &PerpWithdrawReport {
        tag: log_type::PERP_WITHDRAW,
        client_id: client_state.id,
        instr_id: data.instr_id,
        amount: data.amount,  // ❌ Should be: amount
        time: ctx.time,
        ..PerpWithdrawReport::zeroed()
    },
)]);
```

**Impact:** Logs do not reflect actual withdrawals, complicating accounting.


**Recommended Mitigation:** Update the log entry to record the actual withdrawn `amount`.

**Deriverse:** Fixed in commit [2a0fe33](https://github.com/deriverse/protocol-v1/commit/2a0fe336bb2a13bb3e96e1f065b907bc2d3e31bf).

**Cyfrin:** Verified.
