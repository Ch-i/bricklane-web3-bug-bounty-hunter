---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`StakingVault::_deposit` with `minAssetsAmount > DEAD_SHARES` bricks vault
  seeding'
vuln_class: []
---

# `StakingVault::_deposit` with `minAssetsAmount > DEAD_SHARES` bricks vault seeding

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** The first-deposit path burns `DEAD_SHARES = 1000` wei of assets. If `_minAssetsAmount > 1000`, the dead-shares mint reverts `AmountBelowLimit`. The vault cannot be initialized until admin calls `setMinAssetsAmount(<= 1000)` first. Unrecoverable without upgrade if admin fails to sequence correctly.

Source: `issuance/src/vault/StakingVault.sol:190-206, 610-622`.

**Recommended Mitigation:** In `initialize`, `require(_minAssetsAmount <= DEAD_SHARES, ConfigInvalid())`. Or special-case `receiver == BURN` in `_deposit` to skip the min check.

**Syntetika:** Fixed in commit [`3face43`](https://github.com/SyntetikaLabs/monorepo/commit/3face43a003f7feca80d4f5d2086a7695d2ba24c)

**Cyfrin:** Verified.
