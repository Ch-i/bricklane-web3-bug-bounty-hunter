---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: '`WETH` collateral cannot be swapped in `SmartVaultV4`'
vuln_class: []
---

# `WETH` collateral cannot be swapped in `SmartVaultV4`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** [`SmartVaultV4::swap`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L259-L277) allows Smart Vault collateral, specified by its `bytes32` symbol, to be swapped for other supported collateral tokens. The corresponding token address for a given symbol is returned by [`SmartVaultV4::getTokenisedAddr`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L228-L231) based on the output of [`SmartVaultV4::getToken`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L220-L226):

```solidity
function getToken(bytes32 _symbol) private view returns (ITokenManager.Token memory _token) {
    ITokenManager.Token[] memory tokens = ITokenManager(ISmartVaultManagerV3(manager).tokenManager()).getAcceptedTokens();
    for (uint256 i = 0; i < tokens.length; i++) {
        if (tokens[i].symbol == _symbol) _token = tokens[i];
    }
    if (_token.symbol == bytes32(0)) revert InvalidToken();
}

function getTokenisedAddr(bytes32 _symbol) private view returns (address) {
    ITokenManager.Token memory _token = getToken(_symbol);
    return _token.addr == address(0) ? ISmartVaultManagerV3(manager).weth() : _token.addr;
}
```

Native `ETH` is present in the list of accepted tokens; however, it returns `address(0)`. Hence, the symbols for both `ETH` and `WETH` correspond to the `WETH` address which is used as the [`tokenIn`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L265) parameter for the Uniswap V3 Router swap instruction. This is the correct method for swapping native `ETH` via the Uniswap V3 Router which will first [attempt to utilize any native balance](https://github.com/Uniswap/v3-periphery/blob/0682387198a24c7cd63566a2c58398533860a5d1/contracts/base/PeripheryPayments.sol#L58-L61) to cover `amountIn`.

After the swap parameters are populated, execution of the actual swap occurs based on [`SmartVaultV4::executeNativeSwapAndFee`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L233-L237) or [`SmartVaultV4::executeERC20SwapAndFee`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L239-L248), depending on the `inToken` address:

```solidity
inToken == ISmartVaultManagerV3(manager).weth() ?
    executeNativeSwapAndFee(params, swapFee) :
    executeERC20SwapAndFee(params, swapFee);
```

Here, the first conditional branch will be executed if the caller intends to swap `WETH` or native `ETH`; however, this logic assumes that the caller exclusively wants to swap native `ETH`, so it will fail for `WETH` unless the Smart Vault has a sufficient balance of `ETH` to perform a native `ETH` swap.

**Impact:** It is impossible for `WETH` collateral to be swapped directly within a Smart Vault.

**Proof of Concept:** The following test can be added to `SmartVault.js`:

```javascript
it('cant swap WETH', async () => {
  const ethCollateral = ethers.utils.parseEther('0.1')
  await MockWeth.connect(user).deposit({value: ethCollateral});
  await MockWeth.connect(user).transfer(Vault.address, ethCollateral);

  let { collateral } = await Vault.status();
  expect(getCollateralOf('WETH', collateral).amount).to.equal(ethCollateral);

  await expect(
    Vault.connect(user).swap(
      ethers.utils.formatBytes32String('WETH'),
      ethers.utils.formatBytes32String('WBTC'),
      ethers.utils.parseEther('0.05'),
      0)
    ).to.be.revertedWithCustomError(Vault, 'TransferError');
});
```

**Recommended Mitigation:** Consider handling `WETH` with `SmartVaultV4::executeERC20SwapAndFee` by modifying the conditional logic in `SmartRouterV4::swap`:

```diff
-   inToken == ISmartVaultManagerV3(manager).weth() ?
+   _inToken == NATIVE ?
        executeNativeSwapAndFee(params, swapFee) :
        executeERC20SwapAndFee(params, swapFee);
```

**The Standard DAO:** Fixed by commit [`fb965bd`](https://github.com/the-standard/smart-vault/commit/fb965bdee4036cb525e4df18f77ece7b32720a66).

**Cyfrin:** Verified, `WETH` collateral can now be swapped; however, if the output token is specified as `NATIVE` then any existing `WETH` collateral in the Smart Vault will also be withdrawn. Also, `SmartVaultV4::executeNativeSwapAndFee` is now no longer used and can be removed.

**The Standard DAO:** Fixed by commit [`589d645`](https://github.com/the-standard/smart-vault/commit/589d645eae5bc5a10aa0e32302942fcbc5a07491).

**Cyfrin:** Verified, now only the `WETH` output from the swap is withdrawn to native.
