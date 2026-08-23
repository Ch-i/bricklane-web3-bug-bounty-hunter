---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaCrowdfund` has no USDC sweep path; unclaimed refunds and donations
  are permanently stuck'
vuln_class: []
---

# `ArmadaCrowdfund` has no USDC sweep path; unclaimed refunds and donations are permanently stuck

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaCrowdfund::withdrawUnallocatedArm` at `contracts/crowdfund/ArmadaCrowdfund.sol:555` sweeps unclaimed or unsold ARM to treasury in every terminal state. USDC has no counterpart. After `finalize` pushes proceeds to treasury at `:467`, USDC outflows only via `claim, claimRefund` (at `:516, :544`), both gated on per-participant state. USDC no participant claims is permanently stuck in four cases:

1. Success-path: per-participant pro-rata refund (`committed - allocUsdc`) for every non-claimer
2. `refundMode`: full `committed` for every non-claimer (entered when `cappedDemand < MIN_SALE` at `:403` or `totalAllocUsdc_ < MIN_SALE` at `:435`)
3. `Canceled`: full `committed` for every non-claimer
4. Direct USDC donations to the contract

Spec `CROWDFUND.md:393, :401` states refunds do not expire. That guarantees participants are never early-swept; it does not preclude a long-horizon backstop that recovers provably-abandoned funds, matching the ARM recovery pattern.

**Impact:** Worst per-wallet stuck amount is full `committed` under `refundMode` or `Canceled`, reaching the `$15k` hop-0 per-slot cap. Across the `~1,500`-wallet participation cap over multi-year horizons, non-trivial treasury-recoverable capital is lost to abandoned wallets.

**Recommended Mitigation:** Add `withdrawUnallocatedUsdc` mirroring `withdrawUnallocatedArm`'s gating with a deadline equal to or longer than the 3-year ARM claim deadline. Sweep `usdc.balanceOf(address(this))` minus any USDC still owed for refunds; owed is zero once the USDC deadline passes, preserving the refunds-do-not-expire guarantee for any realistic claim window.

**Armada:** Acknowledged.
