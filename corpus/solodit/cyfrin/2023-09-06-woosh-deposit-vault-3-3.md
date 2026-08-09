---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md
tags:
- firm:cyfrin
- report:2023-09-06-woosh-deposit-vault
title: Use != 0 instead of > 0 for unsigned integer comparison
vuln_class: []
---

# Use != 0 instead of > 0 for unsigned integer comparison

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

```solidity
File: DepositVault.sol

38:         require(amount > 0 || msg.value > 0, "Deposit amount must be greater than 0");

38:         require(amount > 0 || msg.value > 0, "Deposit amount must be greater than 0");

39:         if(msg.value > 0)

85:         require(depositToWithdraw.amount > 0, "Deposit has already been withdrawn");

```

**Client:**
Fixed.

**Cyfrin:** Verified in commit [b21d23e](https://github.com/HyperGood/woosh-contracts/commit/b21d23e661b0f25f0e757dc00ee90e4464730b1b).
