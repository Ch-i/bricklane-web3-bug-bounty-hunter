---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-26T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-26-cyfrin-eulerswap-v2-0
title: Vault calls can be done directly to EVC
vuln_class: []
---

# Vault calls can be done directly to EVC

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-26-cyfrin-eulerswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md)_

---

**Description:** In [`FundsLib::depositAssets`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/libraries/FundsLib.sol#L61-L114), two calls are made to the Euler Vault:

* [Line 92](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/libraries/FundsLib.sol#L92):

  ```solidity
  uint256 repaid = IEVault(vault).repay(amount > debt ? debt : amount, p.eulerAccount);
  ```

* [Line 104](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/libraries/FundsLib.sol#L104):

  ```solidity
  try IEVault(vault).deposit(amount, p.eulerAccount) {}
  ```

Both of these function calls are routed through the Ethereum Vault Connector (EVC) via the `callThroughEVC` modifier defined in the Vault:

* [`EVault::repay`](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/EVault.sol#L121):

  ```solidity
  function repay(uint256 amount, address receiver) public virtual override callThroughEVC use(MODULE_BORROWING) returns (uint256) {}
  ```

* [`EVault::deposit`](https://github.com/euler-xyz/euler-vault-kit/blob/master/src/EVault/EVault.sol#L86):

  ```solidity
  function deposit(uint256 amount, address receiver) public virtual override callThroughEVC use(MODULE_VAULT) returns (uint256) {}
  ```

Each call incurs the cost of a contract jump due to the indirection through the Vault contract. To reduce this overhead, these operations can instead be invoked directly on the EVC, as is already done for other vault interactions within `FundsLib`.

**Euler:** Acknowledged.

\clearpage
