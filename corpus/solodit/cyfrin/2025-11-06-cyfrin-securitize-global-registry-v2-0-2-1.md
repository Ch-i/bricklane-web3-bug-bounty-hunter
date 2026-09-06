---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Don't initialize to default values
vuln_class: []
---

# Don't initialize to default values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
registry/GlobalRegistryService.sol
169:        for (uint8 i = 0; i < walletAddresses.length; i++) {
```

**Securitize:** Fixed in commit [5713fd2](https://github.com/securitize-io/bc-global-registry-service-sc/commit/5713fd25851f6a437b45d947f5d4652f2450fb10).

**Cyfrin:** Verified.
