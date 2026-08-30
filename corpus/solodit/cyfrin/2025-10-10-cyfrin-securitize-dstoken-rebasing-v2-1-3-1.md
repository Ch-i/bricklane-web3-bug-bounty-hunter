---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Upgradeable contracts should call `_disableInitializers` in constructor
vuln_class: []
---

# Upgradeable contracts should call `_disableInitializers` in constructor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Upgradeable contracts should [call](https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable#initializing_the_implementation_contract) `_disableInitializers` in constructor:
```solidity
/// @custom:oz-upgrades-unsafe-allow constructor
constructor() {
    _disableInitializers();
}
```

Affected contracts:
* `contracts/bulk/BulkOperator.sol`
* `contracts/compliance/ComplianceConfigurationService.sol`
* `contracts/compliance/ComplianceServiceNotRegulated.sol`
* `contracts/compliance/ComplianceServiceWhitelisted.sol`
* `contracts/compliance/InvestorLockManager.sol`
* `contracts/compliance/LockManager.sol`
* `contracts/compliance/WalletManager.sol`
* `contracts/issuance/TokenIssuer.sol`
* `contracts/multicall/IssuerMulticall.sol`
* `contracts/rebasing/SecuritizeRebasingProvider.sol`
* `contracts/registry/RegistryService.sol`
* `contracts/registry/WalletRegistrar.sol`
* `contracts/swap/SecuritizeSwap.sol`
* `contracts/token/DSToken.sol`
* `contracts/trust/TrustService.sol`
* `contracts/utils/TransactionRelayer.sol`

**Securitize:** Fixed in commit [094baaf](https://github.com/securitize-io/dstoken/commit/094baaf8562cc2eaae1a89769188ad4e8e7476cb); note some of the listed contracts have been removed as they were obsolete.

**Cyfrin:** Verified.
