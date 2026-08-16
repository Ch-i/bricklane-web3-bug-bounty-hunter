---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Prefer `calldata` instead of `memory` for read-only external inputs
vuln_class: []
---

# Prefer `calldata` instead of `memory` for read-only external inputs

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** Prefer `calldata` instead of `memory` for read-only external inputs which also don't get passed to internal functions that need them in `memory`:

* `Agreement.sol`
```solidity
84:    function setProtocolName(string memory _protocolName) external onlyOwner {
91:    function setContactDetails(Contact[] memory _contactDetails) external onlyOwner {
// for `_accounts` only
187:    function addAccounts(string memory _caip2ChainId, Account[] memory _accounts) external onlyOwner {
```

* `ChainValidator.sol`
```solidity
35:    function initialize(address _initialOwner, string[] memory _initialValidChains) external initializer {
```

**SafeHarbor:**
Fixed in commits [d72fd17](https://github.com/PatrickAlphaC/safe-harbor/commit/d72fd17a1e57aa9060f456e2b0d47591de6b9a56), [754edb9](https://github.com/PatrickAlphaC/safe-harbor/commit/754edb9c10e5830a99cf6ada4c8792728b25e2fe).

**Cyfrin:** Verified.
