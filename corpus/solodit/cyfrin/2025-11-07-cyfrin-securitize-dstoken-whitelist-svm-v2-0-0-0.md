---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2-0-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-11-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2-0
title: Unnecessary use of `emit_cpi!` increases CU cost
vuln_class: []
---

# Unnecessary use of `emit_cpi!` increases CU cost

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-07-cyfrin-securitize-dstoken-whitelist-svm-v2.0.md)_

---

**Description:** The `whitelist` instruction uses [`emit_cpi!`](https://github.com/securitize-io/bc-solana-whitelist-sc/blob/main/programs/dstoken-whitelist/src/instructions/whitelist.rs#L247) and the `#[event_cpi]` attribute to emit the `Whitelisted` event.

The `emit_cpi!` macro is designed for programs that are called via CPI and need their events to propagate to calling programs.

However, the `dstoken-whitelist` program is intended to be called directly by end users, not invoked via CPI by other programs.

**Impact:** Using `emit_cpi!` when unnecessary adds complexity without providing any benefit:
- Increases transaction size and CU cost
- It's currently [not possible](https://www.anchor-lang.com/docs/features/events#:~:text=Currently%2C%20event%20data%20emitted%20through%20CPIs%20cannot%20be%20directly%20subscribed%20to.%20To%20access%20this%20data%2C%20you%20must%20fetch%20the%20complete%20transaction%20data%20and%20manually%20decode%20the%20event%20information%20from%20the%20instruction%20data%20of%20the%20CPI.) to directly subscribe to these events
- Requires additional event authority accounts to be passed in the instruction

**Recommended Mitigation:** Consider replacing `emit_cpi!` with `emit!`, and removing the `#[event_cpi]` attribute.

**Securitize:** Here is the fix: https://github.com/securitize-io/bc-solana-whitelist-sc/commit/2a83f4e3f518c9d0801b24d900be56240bd7da31

**Cyfrin:** Verified.
