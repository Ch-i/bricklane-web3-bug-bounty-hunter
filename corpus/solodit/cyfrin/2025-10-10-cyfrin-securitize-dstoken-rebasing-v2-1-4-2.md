---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Use `calldata` for read-only external inputs
vuln_class: []
---

# Use `calldata` for read-only external inputs

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Use `calldata` for read-only external inputs:
* `BulkOperator::bulkIssuance`, `bulkRegisterAndIssuance`, `bulkBurn`
* `TokenIssuer::issueTokens`, `registerInvestor`
* `SecuritizeSwap::nonceByInvestor`, `swap`, `executePreApprovedTransaction`, `doExecuteByInvestor`, `_registerNewInvestor`
* `WalletManager::addIssuerWallets`, `addPlatformWallets`
* `InvestorLockManagerBase::lockInvestor`, `unlockInvestor`, `isInvestorLocked`, `setInvestorLiquidateOnly`, `isInvestorLiquidateOnly` (and similar functions in related classes `IDSLockManager`, `LockManager`)
* `ComplianceConfigurationService::getCountryCompliance`
* `ComplianceServiceRegulated::doPreTransferCheckRegulated`, `completeTransferCheck` for `_services`,

**Securitize:** We:
* deleted a number of these contracts as they were obsolete
* used `calldata` in some places where this wouldn't result in a "stack-too-deep" error.

**Cyfrin:** Verified.
