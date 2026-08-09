---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Enforce minimum transaction amounts in `StakingVault`
vuln_class: []
---

# Enforce minimum transaction amounts in `StakingVault`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Some elaborate vault hacks have involved performing vault transactions using very small amounts such as 1 wei in order to manipulate the vault via rounding.

Normal users will never perform transactions using such small amounts; hence consider enforcing minimum transaction amounts to deprive attackers of this potential attack path.

Since hBTC uses 8 decimals and is 1:1 redeemable for BTC:
* 100000000 = 1 BTC ($118K)
* 10000 = 0.0001 BTC($11.87)

Consider making the minimum transaction limit a configurable parameter that the admin can change as the price of BTC fluctuates, so that it can remain around ~$10 (or even higher if preferred).

The best way to enforce this is likely overriding `ERC4626::_deposit, _withdraw` and reverting inside them if `assets` is smaller than the minimum transaction amount.

**Syntetika:**
Fixed in commit [5ba3c19](https://github.com/SyntetikaLabs/monorepo/commit/5ba3c199cf571679503f8f472769c8efe869a001).

**Cyfrin:** Verified.
