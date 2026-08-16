---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-09-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md
tags:
- firm:cyfrin
- report:2023-09-06-woosh-deposit-vault
title: Use assembly to check for `address(0)`
vuln_class: []
---

# Use assembly to check for `address(0)`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

Saves 6 gas per instance

```solidity
File: DepositVault.sol

40:             require(tokenAddress == address(0), "Token address must be 0x0 for ETH deposits");

45:             require(tokenAddress != address(0), "Token address must not be 0x0 for token deposits");

71:         if(depositToWithdraw.tokenAddress == address(0)){

90:         if(depositToWithdraw.tokenAddress == address(0)){

```
**Client:**
Fixed.

**Cyfrin:** Verified in commit [b21d23e](https://github.com/HyperGood/woosh-contracts/commit/b21d23e661b0f25f0e757dc00ee90e4464730b1b).
