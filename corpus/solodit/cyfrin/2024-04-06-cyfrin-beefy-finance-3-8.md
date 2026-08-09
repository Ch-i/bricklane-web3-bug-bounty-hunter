---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: '`public` functions not used internally could be marked `external`'
vuln_class: []
---

# `public` functions not used internally could be marked `external`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `public` functions not used internally could be marked `external`:

- Found in contracts/protocol/beefy/StratFeeManagerInitializable.sol [Line: 190](contracts/protocol/beefy/StratFeeManagerInitializable.sol#L190)

	```solidity
	    function lockedProfit() public virtual view returns (uint256 locked0, uint256 locked1) {
	```

- Found in contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol [Line: 555](contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L555)

	```solidity
	    function price() public view returns (uint256 _price) {
	```

- Found in contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol [Line: 700](contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L700)

	```solidity
	    function lpToken0ToNative() public view returns (address[] memory) {
	```

- Found in contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol [Line: 709](contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L709)

	```solidity
	    function lpToken1ToNative() public view returns (address[] memory) {
	```

- Found in contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol [Line: 45](contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L45)

	```solidity
	     function initialize(
	```

- Found in contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol [Line: 60](contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L60)

	```solidity
	    function want() public view returns (address _want) {
	```

- Found in contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol [Line: 91](contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L91)

	```solidity
	    function available() public view returns (uint, uint) {
	```

- Found in contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol [Line: 102](contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L102)

	```solidity
	    function previewWithdraw(uint256 _shares) public view returns (uint256 amount0, uint256 amount1) {
	```

- Found in contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol [Line: 116](contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L116)

	```solidity
	    function previewDeposit(uint256 _amount0, uint256 _amount1) public view returns (uint256 shares) {
	```

**Beefy:**
Fixed in commit [139c3f9](https://github.com/beefyfinance/experiments/commit/139c3f9b1f77b78f87f3e1ffe08d79831979ee4e).

**Cyfrin:** Verified.

\clearpage
