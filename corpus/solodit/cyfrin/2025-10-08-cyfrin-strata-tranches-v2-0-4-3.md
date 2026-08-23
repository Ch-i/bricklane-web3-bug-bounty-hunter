---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Missing `Unstaked` event for immediate unstake in `UnstakeCooldown::transfer`
vuln_class: []
---

# Missing `Unstaked` event for immediate unstake in `UnstakeCooldown::transfer`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** When `UnstakeCooldown::transfer` triggers an immediate unstake (i.e. the handler’s call to `proxy.request()` returns `unlockAt <= block.timestamp`), the function returns early after returning the proxy to the pool — but it does not emit the `Unstaked` event for that immediate completion. As a result an on‑chain event is missing for the flow where the redemption happened immediately (no cooldown).

**Impact:** Off-chain systems relying on events for tracking withdrawals may miss these immediate unstake operations. This does not affect on-chain balances or security, and users still receive their funds correctly.

**Recommended Mitigation:** Emit an `Unstaked` (or create a new `ImmediateUnstake`) event in the `transfer()` immediate branch using the `amount` parameter passed to `transfer()`.

**Strata:**
Fixed in commit [c08784](https://github.com/Strata-Money/contracts-tranches/commit/c087849442937e8465f342f9ec6dc82ac4897d0a) by unifying the event being emitted in both cooldown contracts as `Finalized`

**Cyfrin:** Verified.
