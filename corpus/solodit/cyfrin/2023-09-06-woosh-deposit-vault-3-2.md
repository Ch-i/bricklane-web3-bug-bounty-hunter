---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md
tags:
- firm:cyfrin
- report:2023-09-06-woosh-deposit-vault
title: Use Custom Errors
vuln_class: []
---

# Use Custom Errors

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

Instead of using error strings, to reduce deployment and runtime cost, you should use [Custom Errors](https://blog.soliditylang.org/2021/04/21/custom-errors/). This would save both deployment and runtime cost.

```solidity
File: DepositVault.sol

38:         require(amount > 0 || msg.value > 0, "Deposit amount must be greater than 0");

40:             require(tokenAddress == address(0), "Token address must be 0x0 for ETH deposits");

45:             require(tokenAddress != address(0), "Token address must not be 0x0 for token deposits");

60:         require(nonce < deposits.length, "Invalid deposit index");

64:         require(signer == depositToWithdraw.depositor, "Invalid signature");

65:         require(!usedWithdrawalHashes[withdrawalHash], "Withdrawal has already been executed");

66:         require(amount == depositToWithdraw.amount, "Withdrawal amount must match deposit amount");

82:         require(depositIndex < deposits.length, "Invalid deposit index");

84:         require(depositToWithdraw.depositor == msg.sender, "Only the depositor can withdraw their deposit");

85:         require(depositToWithdraw.amount > 0, "Deposit has already been withdrawn");

```
**Client:**
Fixed.

**Cyfrin:** Verified in commit [b21d23e](https://github.com/HyperGood/woosh-contracts/commit/b21d23e661b0f25f0e757dc00ee90e4464730b1b).
