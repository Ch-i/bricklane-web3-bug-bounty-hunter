---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-15
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Consider using a staking rewards distributor to efficiently space out staking
  rewards, further deterring just-in-time attacks
vuln_class: []
---

# Consider using a staking rewards distributor to efficiently space out staking rewards, further deterring just-in-time attacks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Consider using a [staking rewards distributor](https://github.com/ethena-labs/bbp-public-assets/blob/main/contracts/contracts/StakingRewardsDistributor.sol) to efficiently space out staking rewards instead of depositing a large amount in one transaction.

The current code uses a post-withdraw cooldown to deter "just in time" yield attacks where a user front-runs a call to `StakingVault::distributeYield` by depositing a large amount then staking it to get a large amount of the yield.

However this attack can still be executed just that the user must then wait for the cooldown to withdraw which can be as long as 90 days. The cooldown can be set by the admin as low as zero though which would enable "just in time" attacks.

Another option is to perform calls to `StakingVault::distributeYield` via [services](https://docs.flashbots.net/flashbots-protect/overview) designed to prevent front-running.

**Syntetika:**
Acknowledged.
