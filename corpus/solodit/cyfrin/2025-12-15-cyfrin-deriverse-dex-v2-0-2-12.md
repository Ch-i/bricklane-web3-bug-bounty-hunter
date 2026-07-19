---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-12
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: '`get_current_leverage` calculates leverage incorrectly for long positions'
vuln_class: []
---

# `get_current_leverage` calculates leverage incorrectly for long positions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** When calculating the margin, we use `(-(info.funds.min(perp_value as i64))).max(0)`, In a long position, the user’s funds become negative, while in a short position, the `perp_value` becomes negative.

However, when computing leverage, we use `position_size / value`. For long positions, the user’s funds effectively equal the initial funds used to open the position minus the position size, which leads to an incorrect leverage calculation.

Scenerio:
A user with 10,000 USDC in funds who wants to open a 10× long position on Bitcoin, priced at 100,000 USDC.
The user uses the 10,000 USDC as margin and enters a long position of 1 BTC. After the purchase, the user’s funds become –90,000 USDC, and their perpetual position equals 1 BTC.

However, when calculating the current leverage, the function returns 9× instead of 10× because it computes the leverage as follows: `max(-min(-90000, 100000), 0) / 10,000`

**Impact:** This does not have any practical impact because the old and new leverage values are compared in `check_client_leverage_shift`. The logic still holds, as an increase in leverage always results in a higher new leverage, so no issues arise currently.

**Recommended Mitigation:** We should use `perp_value` when calculating the current leverage.


**Deriverse:** Fixed in commit [e4c0a6](https://github.com/deriverse/protocol-v1/commit/e4c0a6fbc8ea72190df0b9e7df16e3db09d99a71).

**Cyfrin:** Verified.
