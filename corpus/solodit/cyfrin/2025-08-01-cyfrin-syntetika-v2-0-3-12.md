---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-12
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Revert if `StakingVault::deposit, mint, redeem, withdraw` would return zero
vuln_class: []
---

# Revert if `StakingVault::deposit, mint, redeem, withdraw` would return zero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** A common tactic of vault exploits is that the vault is manipulated such that:
* `deposit` returns 0 shares (user makes a deposit but gets no shares, effectively donating to the vault)
* `mint` returns 0 assets (user gets shares without depositing assets)
* `redeem` returns 0 assets (user burned their shares but got no assets)
* `withdraw` returns 0 shares (user withdrew assets without burning shares)

There is no legitimate user transaction which should succeed under any of the above conditions; to deny attackers these attack paths, revert if `StakingVault::deposit, mint, redeem, withdraw` would return 0.

**Syntetika:**
Fixed in commit [2e72a57](https://github.com/SyntetikaLabs/monorepo/commit/2e72a57bf8463c7a41d5b4e1c030cf1263507d2f).

**Cyfrin:** Verified.
