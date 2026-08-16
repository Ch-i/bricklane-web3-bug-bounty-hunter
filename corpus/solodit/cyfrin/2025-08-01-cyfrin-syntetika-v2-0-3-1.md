---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Don't initialize to default values in Solidity
vuln_class: []
---

# Don't initialize to default values in Solidity

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Don't initialize to default values in Solidity:
* `Deposit-Registry`:
```solidity
ComplianceChecker.sol
44:        for (uint i = 0; i < complianceOptions.length; i++) {
58:            uint optionIndex = 0;
65:                uint sbtIndex = 0;

CompliantDepositRegistry.sol
133:            uint i = 0;
157:        for (uint i = 0; i < newDepositAddresses.length; i++) {
200:        for (uint i = 0; i < batchLength; i++) {
```

**Syntetika:**
Fixed in commit [7c69e94](https://github.com/SyntetikaLabs/monorepo/commit/7c69e94d165cfe4b78ace518d622e25654e482d3).

**Cyfrin:** Verified.
