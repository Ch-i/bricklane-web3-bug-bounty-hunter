---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-13
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Margin call limit bypass
vuln_class: []
---

# Margin call limit bypass

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The limit check for margin calls can be bypassed, allowing the total number of margin calls to exceed `MAX_MARGIN_CALL_TRADES`.

The issue occurs because after the first `check_{short,long}_margin_call`, the trade counter is reset in next `check_{short,long}_margin_call` tha allow to execute additional trades beyond the intended limit.

Example:
`MAX_MARGIN_CALL_TRADES` is set to 10.
`check_short_margin_call` returns 9 (meaning 9 margin calls were executed).
Since 9 < 10, `check_long_margin_call` is then called.
`check_long_margin_call` executes an additional 10 margin calls.

As a result, a total of 9 + 10 = 19 margin calls are executed, which exceeds the intended limit of 10.

**Impact:** The `MAX_MARGIN_CALL_TRADES` limit can be exceeded, which may also lead to more execution costs.

**Recommended Mitigation:** Track the cumulative margin-call count across both functions and compare it to MAX_MARGIN_CALL_TRADES before executing any additional margin calls.

**Deriverse:** Fixed in commit [4f7bc8](https://github.com/deriverse/protocol-v1/commit/4f7bc8ac68325aa93b339ff91c0ac794ea17ffd9).

**Cyfrin:** Verified.
