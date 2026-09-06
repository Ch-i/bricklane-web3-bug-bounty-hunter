---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-13
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Refactor duplicated checks into modifiers
vuln_class: []
---

# Refactor duplicated checks into modifiers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Refactor duplicated checks into modifiers:
* `contracts/compliance/LockManager.sol`
```solidity
// 1) invalid address
compliance/InvestorLockManager.sol
60:        require(_to != address(0), "Invalid address");
108:        require(_to != address(0), "Invalid address");
132:        require(_who != address(0), "Invalid address");
152:        require(_who != address(0), "Invalid address");

compliance/LockManager.sol
96:        require(_to != address(0), "Invalid address");
109:        require(_to != address(0), "Invalid address");
144:        require(_who != address(0), "Invalid address");
159:        require(_who != address(0), "Invalid address");

token/TokenLibrary.sol
76:        require(_params._to != address(0), "Invalid address");
142:        require(_from != address(0), "Invalid address");
143:        require(_to != address(0), "Invalid address");

// 2) invalid time
compliance/ComplianceServiceNotRegulated.sol
65:        require(_time > 0, "Time must be greater than zero");

compliance/InvestorLockManager.sol
177:        require(_time > 0, "Time must be greater than zero");

compliance/ComplianceServiceWhitelisted.sol
116:        require(_time > 0, "Time must be greater than zero");

compliance/LockManager.sol
169:        require(_time > 0, "Time must be greater than zero");

compliance/ComplianceServiceRegulated.sol
706:        require(_time != 0, "Time must be greater than zero");

// 3) max number of wallets
compliance/WalletManager.sol
74:        require(_wallets.length <= 30, "Exceeded the maximum number of wallets");
96:        require(_wallets.length <= 30, "Exceeded the maximum number of wallets");
```

**Securitize:** **Cyfrin:**
