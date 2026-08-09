---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-10
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`StakingVault::_withdraw` resets `$.lastDistributionTimestamp` to 0'
vuln_class: []
---

# `StakingVault::_withdraw` resets `$.lastDistributionTimestamp` to 0

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** When the post-withdraw total supply falls to `DEAD_SHARES`, the code zeroes `vestingAmount` and `lastDistributionTimestamp`. Setting `lastDistributionTimestamp = 0` is unusual - `getUnvestedAmount` later computes `block.timestamp - lastDistributionTimestamp` which will produce a huge number, but since `vestingAmount = 0` the product is also 0. Relies on a non-obvious invariant.

**Recommended Mitigation:** Either drop the `lastDistributionTimestamp = 0` write (only `vestingAmount = 0` is needed to make `getUnvestedAmount` return 0) or document the invariant.

**Syntetika:** Fixed in commit [`72caefc`](https://github.com/SyntetikaLabs/monorepo/commit/72caefc262a2f20bbb265fbfadb1f958b5c63dae)

**Cyfrin:** Verified. `lastDistributionTimestamp = 0`  dropped.
