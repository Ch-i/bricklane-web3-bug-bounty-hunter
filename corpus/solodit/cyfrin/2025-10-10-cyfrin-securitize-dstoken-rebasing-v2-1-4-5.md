---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-5
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
title: Use named return variables where this optimizes away a local variable definition
vuln_class: []
---

# Use named return variables where this optimizes away a local variable definition

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Use named return variables where this optimizes away a local variable definition, then also remove the final obsolete `return` statement:
* `StandardToken::balanceOf`, `totalSupply`
* `DSToken::totalIssued`, `balanceOfInvestor`, `getCommonServices`
* `TokenLibrary::issueTokensCustom`, `issueTokensWithNoCompliance`, `burn`
* `RegistryService::getInvestorDetailsFull`
* `SecuritizeSwap::calculateDsTokenAmount`
* `MulticallProxy::_slice`, `_callTarget`
* `LockManager::getTransferableTokens`
* `InvestorLockManager::getTransferableTokens`
* `ComplianceConfigurationService::getAll`

**Securitize:** Acknowledged.
