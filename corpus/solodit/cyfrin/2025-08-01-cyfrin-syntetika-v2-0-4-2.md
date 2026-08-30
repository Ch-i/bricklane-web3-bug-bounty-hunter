---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-4-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Use named return variables when this eliminates local variables
vuln_class: []
---

# Use named return variables when this eliminates local variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Use named return variables when this eliminates local variables:
* `CompliantDepositRegistry::getDepositAddresses`
* `StakingVault::redeem`

**Syntetika:**
Fixed in commit [f8f821d](https://github.com/SyntetikaLabs/monorepo/commit/f8f821de057517f9b94963607050b6da2ee647a3).

**Cyfrin:** Verified.
