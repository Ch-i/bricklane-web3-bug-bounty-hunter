---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-4-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers
vuln_class: []
---

# Use `ReentrancyGuardTransient` for faster `nonReentrant` modifiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Use [ReentrancyGuardTransient](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/ReentrancyGuardTransient.sol) for faster `nonReentrant` modifiers:
* `issuance/src/minter/Minter.sol`

**Syntetika:**
Fixed in commit [d5131f6](https://github.com/SyntetikaLabs/monorepo/commit/d5131f6dba14b2595fae28e34065cb05abb9ed36).

**Cyfrin:** Verified.
