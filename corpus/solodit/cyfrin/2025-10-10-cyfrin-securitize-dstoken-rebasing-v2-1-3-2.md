---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Prefer explicit unsigned integer sizes
vuln_class: []
---

# Prefer explicit unsigned integer sizes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Prefer explicit unsigned integer sizes:
```solidity
trust/TrustService.sol
218:        for (uint i = 0; i < _addresses.length; i++) {

compliance/ComplianceConfigurationService.sol
34:        for (uint i = 0; i < _countries.length; i++) {

compliance/WalletManager.sol
75:        for (uint i = 0; i < _wallets.length; i++) {
97:        for (uint i = 0; i < _wallets.length; i++) {

```

**Securitize:** Fixed in commit [26c5bb0](https://github.com/securitize-io/dstoken/commit/26c5bb05676233ca0c5caa1d9b02fd98360ad4e7).

**Cyfrin:** Verified.
