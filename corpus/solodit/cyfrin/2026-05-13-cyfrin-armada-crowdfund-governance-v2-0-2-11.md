---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-11
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaRedemption` has no sweep path; assets pro-rata to never-redeemed ARM
  are permanently stuck'
vuln_class: []
---

# `ArmadaRedemption` has no sweep path; assets pro-rata to never-redeemed ARM are permanently stuck

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaRedemption::redeem` at `contracts/governance/ArmadaRedemption.sol:118-190` distributes treasury assets pro-rata via `share = (available * armAmount) / circulating` at `:164` (and the equivalent ETH calculation at `:175`). The contract has no sweep, recovery, or rescue function — `IERC20` and `ETH` only flow out via `redeem`.

Two mechanisms leave assets permanently stuck:

1. **Per-call integer-division dust.** Each `share` rounds down. Dust per call is bounded and self-correcting only if 100% of circulating ARM eventually redeems — when the final holder's `armAmount == circulating`, `share = available` sweeps the residual cleanly.

2. **ARM that never redeems (dominant).** Lost keys, dormant addresses, and contracts holding ARM that cannot or will not call `redeem` leave their pro-rata share of every swept asset stranded forever. If `F` is the fraction of circulating ARM that never redeems, `F` of every USDC/ETH/other-token amount swept into the contract is permanently stuck. There is no deadline, no claim-window expiry, no backstop. Once redemption activity ceases, the residual is unrecoverable.

`specs/GOVERNANCE.md` §Wind-Down §Redemption mechanism specifies the redemption is permissionless with no deadline ("Deposit ARM, receive your share, whenever you want"). The spec is silent on what happens to assets corresponding to never-redeemed ARM — silence on a backstop, not an explicit prohibition. A long-horizon recovery path is consistent with the no-deadline guarantee for any realistic claim window.

**Impact:** Treasury value proportional to the lost-key / dormant-holder fraction of circulating ARM is permanently locked in `ArmadaRedemption`. Industry-typical lost-key rates for long-lived tokens range from 5-20%; over a multi-year post-wind-down horizon, the stuck fraction is material relative to the swept treasury.

**Recommended Mitigation:** Add a long-horizon deadline-gated sweep, e.g. `sweepResidual(address token)` callable any time after `triggerTime + RESIDUAL_DELAY` where `RESIDUAL_DELAY` is years (3-5 years preserves the no-deadline spirit for any realistic redeemer). Recipient choice is constrained because the treasury is wound down by definition — viable options:

1. Distribute the residual pro-rata to the final-N redeemers via a claim ledger.
2. Direct to a community-controlled multisig address fixed at deployment.
3. Permanently burn (where supported) or send to `address(0)`-equivalent for the asset.

Pick whichever aligns with the protocol's social-recovery norms; the key property is that an upper-bound fraction of treasury is no longer mathematically frozen for non-claiming holders.

**Armada:** Acknowledged.
