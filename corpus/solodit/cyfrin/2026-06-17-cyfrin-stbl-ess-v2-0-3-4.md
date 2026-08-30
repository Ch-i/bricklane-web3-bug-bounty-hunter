---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_ESS_Wrapper1` initializer missing `sum(ratios) == FEES_CONSTANT` check
  allows permanent basket misconfiguration, silently corrupting all subsequent ESS
  deposits'
vuln_class: []
---

# `STBL_ESS_Wrapper1` initializer missing `sum(ratios) == FEES_CONSTANT` check allows permanent basket misconfiguration, silently corrupting all subsequent ESS deposits

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_Wrapper1::__STBL_ESS_Wrapper1_init_unchained` configures the asset basket by iterating over a caller-supplied `_ratios` array. Each entry is validated individually — `if (_ratios[i].ratio > FEES_CONSTANT) revert` — but there is no check that the aggregate sum equals `FEES_CONSTANT` (10^9). - SPEC §7.1 explicitly requires this: *"All asset allocation ratios in a basket must sum to `FEES_CONSTANT`."*

`iCalculateRatios(_amt)` allocates a user's deposit across assets using these ratios: `individualAmts[i] = _amt * Ratios[assetID].ratio / FEES_CONSTANT`. If the sum of all ratios deviates from `FEES_CONSTANT`, the total allocated across assets differs from `_amt`.
- When the sum is less than `FEES_CONSTANT`, a portion of the intended deposit is silently unallocated — users deposit less total asset value than the `_amt` parameter implies and receive proportionally less ESS.
- When the sum exceeds `FEES_CONSTANT`, users are silently over-charged, as more total asset value is pulled than `_amt` implies.

In both cases ESS minting remains correctly backed by the actual USST delta, so the ESS collateral invariant holds; what breaks is the basket composition invariant and the expected deposit behaviour.

**Recommended Mitigation:** Accumulate a running sum in the init loop and assert equality with `FEES_CONSTANT` after the loop before the function returns.

**STBL:** Fixed in commit [983f5f3](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/983f5f332a215c932550a505c6a06f4847e749ea).

**Cyfrin:** Verified. The `initializer` now accumulates a running `raitoSum` across all ratio entries and reverts with `STBL_InvalidFeePercentage` if the total does not equal `FEES_CONSTANT` after the loop.
