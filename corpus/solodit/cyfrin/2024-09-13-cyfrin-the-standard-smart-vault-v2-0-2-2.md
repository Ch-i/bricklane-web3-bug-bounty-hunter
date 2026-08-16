---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Removal of Hypervisor data locks deposited Smart Vault collateral
vuln_class: []
---

# Removal of Hypervisor data locks deposited Smart Vault collateral

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** A Gamma Vault (aka Hypervisor) is an external contract that maintains and offers fungible shares in Uniswap V3 liquidity positions. The Standard leverages multiple Hypervisors to enable the collateral backing `USDs` to earn yield, configured by admin calls to [`SmartVaultYieldManager::addHypervisorData`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L222-L224). When Smart Vault collateral is deposited into one of these Hypervisors, it is minted Hypervisor ERC-20 tokens to represent a share of the underlying position and internally calls [`SmartVaultV4::addUniqueHypervisor`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L279-L284) to maintain a list of Hypervisors in which it has collateral deposited.

If an admin call is made to [`SmartVaultYieldManager::removeHypervisorData`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L226-L228) to remove a Hypervisor in which Smart Vaults still have open positions, the underlying collateral will be locked. This is due to the following validation in [`SmartVaultYieldManager::_withdrawOtherDeposit`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L202-L207) that requires the Hypervisor data to be valid and configured:

```solidity
function _withdrawOtherDeposit(address _hypervisor, address _token) private {
    HypervisorData memory _hypervisorData = hypervisorData[_token];
    if (_hypervisorData.hypervisor != _hypervisor) revert IncompatibleHypervisor();
    /* snip: withdraw and swap */
}
```

However, this collateral locked in the removed Hypervisor will still contribute to the collateral calculation of the Smart Vault due to looping over its independently maintained `SmartVaultV4::hypervisors` array (from which Hypervisors are only removed when collateral is withdrawn).

**Impact:** Hypervisor tokens and the corresponding Smart Vault collateral can be locked indefinitely unless the protocol admin re-adds the Hypervisor data, ignoring a separate finding detailing the malicious removal of Hypervisor tokens from Smart Vaults.

**Proof of Concept:** The following test can be added to `SmartVault.js`:
```javascript
it('locks collateral when hypervisor is removed', async () => {
  const ethCollateral = ethers.utils.parseEther('0.1')
  await user.sendTransaction({ to: Vault.address, value: ethCollateral });

  let { collateral, totalCollateralValue } = await Vault.status();
  let preYieldCollateral = totalCollateralValue;
  expect(getCollateralOf('ETH', collateral).amount).to.equal(ethCollateral);

  depositYield = Vault.connect(user).depositYield(ETH, HUNDRED_PC.div(10));
  await expect(depositYield).not.to.be.reverted;
  await expect(depositYield).to.emit(YieldManager, 'Deposit').withArgs(Vault.address, MockWeth.address, ethCollateral, HUNDRED_PC.div(10));

  ({ collateral, totalCollateralValue } = await Vault.status());
  expect(getCollateralOf('ETH', collateral).amount).to.equal(0);
  expect(totalCollateralValue).to.equal(preYieldCollateral);

  await YieldManager.connect(admin).removeHypervisorData(MockWeth.address);

  // collateral is still counted
  ({ collateral, totalCollateralValue } = await Vault.status());
  expect(getCollateralOf('ETH', collateral).amount).to.equal(0);
  expect(totalCollateralValue).to.equal(preYieldCollateral);

  // user cannot remove collateral
  await expect(Vault.connect(user).withdrawYield(MockWETHWBTCHypervisor.address, ETH))
    .to.be.revertedWithCustomError(YieldManager, 'IncompatibleHypervisor');
});
```

**Recommended Mitigation:** If it is necessary to have the ability to remove Hypervisors, consider also allowing Smart Vault owners to remove Hypervisor tokens from their Vaults if they have been delisted from `SmartVaultYieldManager`, with a check that they are still sufficiently collateralized.

**The Standard DAO:** Acknowleged, not fixed as we believe a user can remove with `removeAsset()`. As long as the vault remains collateralised, there shouldn’t be a problem. We are also not intending to remove Hypervisors if we can avoid it.

**Cyfrin:** Acknowledged, while removed Hypervisor tokens will continue to contribute to the collateralization value of a given Smart Vault, they can be removed by calling `SmartVaultV4::removeAsset` so long as the Vault remains sufficiently collateralized.
