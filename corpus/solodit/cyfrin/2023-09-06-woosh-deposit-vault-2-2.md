---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md
tags:
- firm:cyfrin
- report:2023-09-06-woosh-deposit-vault
title: Functions not used internally could be marked external
vuln_class: []
---

# Functions not used internally could be marked external

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

**Severity:** Informational

**Description:** Using proper visibility modifiers is a good practice to prevent unintended access to functions.
Furthermore, marking functions as `external` instead of `public` can save gas.

```solidity
File: DepositVault.sol

37:     function deposit(uint256 amount, address tokenAddress) public payable

59:     function withdraw(uint256 amount, uint256 nonce, bytes memory signature, address payable recipient) public

81:     function withdrawDeposit(uint256 depositIndex) public
```

**Recommended Mitigation:** Consider change the visibility modifier to `external` for the functions that are not used internally.

**Client:**
Fixed.

**Cyfrin:** Verified in commit [b21d23e](https://github.com/HyperGood/woosh-contracts/commit/b21d23e661b0f25f0e757dc00ee90e4464730b1b).
