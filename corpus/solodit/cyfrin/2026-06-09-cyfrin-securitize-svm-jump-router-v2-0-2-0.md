---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Recomputed power-of-ten divisor in repeated per-swap price denormalization
vuln_class: []
---

# Recomputed power-of-ten divisor in repeated per-swap price denormalization

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The shared swap implementation repeatedly calls `denormalize_price_to_decimals` with the same decimal value during event emission.

On the standard operator-gated path, `nbbo_price_opt` is `Some`, so both NBBO and JUMP prices are denormalized in the buy direction (`programs/bc-solana-jump-router-sc/src/instructions/swap_accounts.rs:393-404`) and in the sell direction (`swap_accounts.rs:583-594`). Each call recomputes `10u128.pow(scale_diff)` inside `denormalize_price_to_decimals` (`programs/bc-solana-jump-router-sc/src/utils/swap_utils.rs:77-84`).

On the headless path, `nbbo_price_opt` is `None`, so only the JUMP price is denormalized. The repeated computation therefore applies to standard swaps, while headless swaps pay the cost once per swap.

**Impact:** This is a small per-swap compute inefficiency on standard swaps. It has no correctness impact.

**Recommended Mitigation:** If the optimization is worth the added code, compute the scale divisor once and use it for both NBBO and JUMP price denormalization. Alternatively, leave the current implementation for readability.

**Securitize:** Acknowledged; The impact is negligible.

\clearpage
