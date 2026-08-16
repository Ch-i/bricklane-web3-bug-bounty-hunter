---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Inability for users to permissionlessly stake and earn yield
vuln_class: []
---

# Inability for users to permissionlessly stake and earn yield

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** The intention of the protocol as specified in the kick-off call and in discussion with the client is that users should be able to permissionlessly:
* buy hBTC from a decentralized exchange
* stake/unstake hBTC in a permissionless manner via `StakingVault`

**Impact:** In the current implementation `StakingVault` uses `onlyWhitelisted` modifiers on many core functions which prohibits users who permissionlessly bought hBTC using a decentralized exchange from subsequently staking their hBTC and earning yield.

To enable this the admin would need to call `setGlobalWhitelist` which would effectively disable the whitelist and compliance checks anyway.

**Recommended Mitigation:** Consider using only the "blacklist" functionality in `StakingVault` but removing the "whitelist" functionality to allow users to permissionlessly participate in staking and earning yield.

**Syntetika:**
Fixed in commit [86384fe](https://github.com/SyntetikaLabs/monorepo/commit/86384fe1504780338649d25f720fb78b25132875).

**Cyfrin:** Verified.
