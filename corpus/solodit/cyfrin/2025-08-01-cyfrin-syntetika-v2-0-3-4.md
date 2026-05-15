---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Consider using `SafeCast` when downcasting amounts
vuln_class: []
---

# Consider using `SafeCast` when downcasting amounts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Consider using [SafeCast](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeCast.sol) when downcasting amounts:
* `StakingVault.sol`:
```solidity
144:        cooldowns[msg.sender].underlyingAmount += uint152(assetsRedeemed);
165:        cooldowns[msg.sender].underlyingAmount += uint152(assets);
```

**Syntetika:**
Fixed in commit [8d7987c](https://github.com/SyntetikaLabs/monorepo/commit/8d7987cfe72ab33c51b486fd3ac5fe2670292a30).

**Cyfrin:** Verified.
