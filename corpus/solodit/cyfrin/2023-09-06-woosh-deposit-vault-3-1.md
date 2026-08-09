---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-06-woosh-deposit-vault-3-1
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
title: Use calldata instead of memory for function arguments that do not get mutated
vuln_class: []
---

# Use calldata instead of memory for function arguments that do not get mutated

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-06-Woosh Deposit Vault.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-06-Woosh%20Deposit%20Vault.md)_

---

Mark data types as `calldata` instead of `memory` where possible. This makes it so that the data is not automatically loaded into memory. If the data passed into the function does not need to be changed (like updating values in an array), it can be passed in as `calldata`. The one exception to this is if the argument must later be passed into another function that takes an argument that specifies `memory` storage.

```solidity
File: DepositVault.sol

55:     function getWithdrawalHash(Withdrawal memory withdrawal) public view returns (bytes32)

59:     function withdraw(uint256 amount, uint256 nonce, bytes memory signature, address payable recipient) public

```
**Client:**
Acknowledged.

**Cyfrin:** Acknowledged.
