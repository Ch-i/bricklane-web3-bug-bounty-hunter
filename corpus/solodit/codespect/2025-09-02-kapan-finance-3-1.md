---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-3-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[I-02] Some transfers don’t confirm the return boolean'
vuln_class: []
---

# [I-02] Some transfers don’t confirm the return boolean

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Original severity:** Best Practices

**Description:**

Throughout the protocol, `transfer(...)` and `transfer_from(...)` functions returns are checked to be true. However, there are a few instances where this doesn’t happen:

1. `RouterGateway.cairo`:
   - In `after_send_instructions(...)` function under `Withdraw` and `Repay` instructions.
2. `NostraGateway.cairo`:
   - In `repay(...)` function when transferring the `underlying_token`.
3. `vesu_gateway.cairo`:
   - In `repay(...)` function when transferring any `remainder` amount.

**Status:** Fixed
