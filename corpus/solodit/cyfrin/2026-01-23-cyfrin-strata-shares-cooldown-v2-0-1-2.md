---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: finalizeWithFee lacks race conditioning protection
vuln_class: []
---

# finalizeWithFee lacks race conditioning protection

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** `finalizeWithFee` does not provide any user-defined bounds on the resulting fee or claimed amount, making the outcome sensitive to state changes between transaction submission and execution. The effective fee can change
if new requests are merged (especially when hitting the 70th slot), if `vaultEarlyExitFeePerDay` is updated, or if the execution crosses a day boundary which increases `daysLeft`.

Additionally, reordering of requests due to `cancel/finalize` can change which request index is finalized, potentially causing unexpected reverts. As a result, users cannot reliably predict or cap the cost of early finalization at the time they sign the transaction.

**Recommended Mitigation:** Allow users to specify explicit bounds (e.g. maxFee) when calling `finalizeWithFee` and revert if those bounds are violated. This provides slippage-style protection against fee changes, timing effects, and request mutations.

**Strata:** Fixed in commit [092a08b](https://github.com/Strata-Money/contracts-tranches/commit/092a08b9fd0b79f3f7fa2461cb277113db121c8d).

**Cyfrin:** Verified. Now, users can input slippage protection when calling `finalizeWithFee`. The slippage protection is optional; users can choose not to specify it and accept the calculated values at execution time.

\clearpage
