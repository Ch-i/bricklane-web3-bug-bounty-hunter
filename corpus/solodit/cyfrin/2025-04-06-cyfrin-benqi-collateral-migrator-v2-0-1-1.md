---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-06-cyfrin-benqi-collateral-migrator-v2-0-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-06-cyfrin-benqi-collateral-migrator-v2-0
title: NatSpec `@custom:reverts` inconsistencies
vuln_class: []
---

# NatSpec `@custom:reverts` inconsistencies

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md)_

---

**Description:** Below are some inconsistencies in how the NatSpec `@custom:reverts` are formatted:

* [`CollateralMigrator::LBFlashLoanCallback`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/CollateralMigrator.sol#L438-L442):
  ```solidity
  * @custom:reverts IncorrectToAsset Thrown if the `toAsset` in `swapParams` does not match the target market's base token.
  * @custom:reverts RedeemFailed Thrown if the QiToken redemption process fails.
  * - {MintFailed}: Thrown if the minting of tokens to the target market fails.
  * @custom:reverts MintFailed Thrown if the minting of tokens to the target market fails.
  * @custom:reverts InvalidCallbackHash Thrown if the callback data hash does not match the stored hash.
  ```
  `MintFailed` is mentioned twice, once with `@custom:reverts` once without.

* [`SwapModule::constructor`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/modules/SwapModule.sol#L62-L72)
  ```solidity
  /**
   * @notice Initializes the SwapModule with the address of the 1Inch router.
   * @param _swapRouter The address of the 1Inch router contract.
   * @dev Reverts with {InvalidZeroAddress} if `_swapRouter` is the zero address.
   */
  constructor(address _swapRouter) {
      if (_swapRouter == address(0)) {
          revert InvalidZeroAddress();
      }
      SWAP_ROUTER = _swapRouter;
  }
  ```
  The custom error `InvalidZeroAddress` is missing the `@custom:reverts` in the documentation.

* [`SwapModule::_swap`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/modules/SwapModule.sol#L84-L86)
  ```solidity
  * - {SwapFailed} if the call to the 1Inch router fails.
  * - {IncorrectSwapAmount} if the resulting balance does not increase.
  * - {OutputLessThanMinAmount} if the received amount is less than the specified minimum.
  ```
  The `@custom:reverts` is not used as it is in `CollateralMigrator`

**Benqi:** Fixed in commit [`053f28a`](https://github.com/woof-software/benqi-collateral-migrator/commit/053f28a6f303d97335a87b46edc2864a379ed098)

**Cyfrin:** Verified.

\clearpage
