---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Blacklisted users can claim withdrawn assets after the cooldown period
vuln_class: []
---

# Blacklisted users can claim withdrawn assets after the cooldown period

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `StakingVault::_update` uses modifiers `notBlacklisted(from) notBlacklisted(to)` to prevent blacklisted users from performing most actions.

But `StakingVault::claimWithdraw` does not use the `notBlacklisted` modifier. Hence a user who has been blacklisted after they first withdrew/redeemed can still claim those assets once the cooldown period has expired.

**Recommended Mitigation:** `StakingVault::claimWithdraw` should have at least `notBlacklisted(msg.sender)` and possibly also `notBlacklisted(receiver)`, though the second one is less effective since the user can input an arbitrary address.

**Syntetika:**
Fixed in commit [d98afbf](https://github.com/SyntetikaLabs/monorepo/commit/d98afbfd76670a0cbebfb3399f167481344f689d).

**Cyfrin:** Verified.
