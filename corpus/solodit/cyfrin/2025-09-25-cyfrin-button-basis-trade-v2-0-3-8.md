---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Use named mapping parameters to explicitly note the purpose of keys and values
vuln_class: []
---

# Use named mapping parameters to explicitly note the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** Use named mapping parameters to explicitly note the purpose of keys and values:

* [`BasisTradeTailor`](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/BasisTradeTailor.sol#L41-L47)
  ```solidity
  // Mappings
  /// @notice Maps pocket address to the user who controls it
  mapping(address => address) public pocketUser;
  /// @notice Tracks pending withdrawal amounts for each pocket
  mapping(address => uint256) public withdrawalRequests;
  /// @notice Whitelist of addresses allowed to create pockets
  mapping(address => bool) public creationWhitelist;
  ```

* [`BasisTradeVault`](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/BasisTradeVault.sol#L80):
  ```solidity
  mapping(address => bool) public depositWhitelist;
  ```

* [`PocketFactory`](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/PocketFactory.sol#L28):
  ```solidity
  mapping(address => bool) public approvedTailors;
  ```

**Button:** Fixed in commit [`a9ba276`](https://github.com/buttonxyz/button-protocol/commit/a9ba276e0536c38f8a89fb1105ca7f3a0d918519)

**Cyfrin:** Verified.
