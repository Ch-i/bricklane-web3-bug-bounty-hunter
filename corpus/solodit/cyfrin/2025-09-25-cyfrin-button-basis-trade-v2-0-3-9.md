---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-9
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Remove obsolete return statements when using named return variables
vuln_class: []
---

# Remove obsolete return statements when using named return variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** Remove either the named return value or the `return` statement.

* [`BasisTradeVault::requestWithdraw`](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/BasisTradeVault.sol#L396-L404)
  ```solidity
  function requestWithdraw(uint256 assets) external returns (uint256 queuePosition) {
      // ...

      return requestRedeem(shares);
  }
  ```

* [BasisTradeVault::](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/BasisTradeVault.sol#L412-L444)
  ```solidity
  function requestRedeem(uint256 shares) public requirePocket returns (uint256 queuePosition) {
      // ...

      return queuePosition;
  }
  ```

* [`Pocket::exec`](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/Pocket.sol#L94-L106)
  ```solidity
  function exec(address target, bytes calldata data) external onlyOwner returns (bytes memory result) {
      // ...

      return result;
  }
  ```

**Button:** Fixed in commit [`9d8ed75`](https://github.com/buttonxyz/button-protocol/commit/9d8ed75bd5ed4957c7b23f9b06ff362b7bb218a4)

**Cyfrin:** Verified.

\clearpage
