---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Missing sanity check for reasonable duration values
vuln_class: []
---

# Missing sanity check for reasonable duration values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** `StakingVault::initialize` and `StakingVaultFactory::deployVault` fail to validate that lock durations are reasonable (not zero, not extremely large).

Admin could accidentally set `minLockDuration = 0` or both `minLockDuration` and `maxLockDuration` to extremely high values as long as `minLockDuration` is less or equal to `maxLockDuration`.

**Recommended Mitigation:** Add a sanity check to prevent durations that are not reasonable. Use constants to determine an acceptable range of values.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
