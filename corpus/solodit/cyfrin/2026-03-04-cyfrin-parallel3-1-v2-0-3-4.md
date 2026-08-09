---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Mint and burn fees are distributed via `Surplus`
vuln_class: []
---

# Mint and burn fees are distributed via `Surplus`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** [PR-13](https://github.com/parallel-protocol/parallel-parallelizer/pull/13) description defines expected behaviour of `Surplus` module:
>The issue: When yield-bearing assets (e.g., sUSDe, etc.) are deposited as collateral, their balance increases as yield accrues. However, the normalizedStables tracking only reflects the stablecoins originally issued against the collateral, not the additional value from accrued yield. This creates a surplus where the actual collateral value exceeds the tracked backing.

>Solution: The processSurplus function calculates this surplus (difference between current collateral value and normalized stables), swaps the surplus collateral into TokenP, and then the TokenP can be released to corresponding payees set by the Governor via the release() function.

However there is another unmentioned source that generates value: mint and burn fees. During mint it takes collateral amount higher than minted USDP, opposite in burn: it sends slightly less collateral then USDP burnt. So actually `Surplus` treats those generated fees as surplus and distributes it.

**Recommended Mitigation:** Consider documenting such behaviour.

**Parallel:** Fixed by updating [PR [*Insufficient validation of collateral consumption in external swap during Harvesting in `GenericHarvester`*](#insufficient-validation-of-collateral-consumption-in-external-swap-during-harvesting-in-genericharvester)'s description](https://github.com/parallel-protocol/parallel-parallelizer/pull/13#issue-3793312640)

**Cyfrin:** Verified.
