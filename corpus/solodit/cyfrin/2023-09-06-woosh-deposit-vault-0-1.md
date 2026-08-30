---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md
tags:
- firm:cyfrin
- report:2023-09-06-woosh-deposit-vault
title: Use call instead of transfer
vuln_class: []
---

# Use call instead of transfer

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

**Severity:** Medium

**Description:** In both of the withdraw functions, `transfer()` is used for native ETH withdrawal.
The transfer() and send() functions forward a fixed amount of 2300 gas. Historically, it has often been recommended to use these functions for value transfers to guard against reentrancy attacks. However, the gas cost of EVM instructions may change significantly during hard forks which may break already deployed contract systems that make fixed assumptions about gas costs. For example. EIP 1884 broke several existing smart contracts due to a cost increase of the SLOAD instruction.

**Impact:** The use of the deprecated transfer() function for an address will inevitably make the transaction fail when:
- The claimer smart contract does not implement a payable function.
- The claimer smart contract does implement a payable fallback which uses more than 2300 gas unit.
- The claimer smart contract implements a payable fallback function that needs less than 2300 gas units but is called through proxy, raising the call's gas usage above 2300.

Additionally, using higher than 2300 gas might be mandatory for some multisig wallets.

**Recommended Mitigation:** Use call() instead of transfer().

**Protocol:**
Agree, transfer was causing issues with smart contract wallets.

**Cyfrin:** Verified in commit [7726ae7](https://github.com/HyperGood/woosh-contracts/commit/7726ae72118cfdf91ceb9129e36662f69f4d42de).
