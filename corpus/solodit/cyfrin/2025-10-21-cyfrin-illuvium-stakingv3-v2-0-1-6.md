---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Lack of validation of `Pool.underlyingToken == StakingVault.stakingAsset`
vuln_class: []
---

# Lack of validation of `Pool.underlyingToken == StakingVault.stakingAsset`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** `L2RevenueDistributorV3::_computeReserveUnits` decides whether a Vault pool is an ILV vault or an LP vault based on `pool.underlyingToken`. However, there is no check that this value actually matches the vault’s true staking asset (`StakingVault.stakingAsset`). A mismatch (by config error or upgrade) would cause the distributor to compute reserve units against the wrong token/pair, skewing reserve-weighted rewards.

Consider validating on pool creation/update that, for `PoolKind.Vault`, `pool.underlyingToken == StakingVault(recipient).stakingAsset()`. Alternatively, remove `underlyingToken` from config for Vault pools and always read the asset from the vault.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
