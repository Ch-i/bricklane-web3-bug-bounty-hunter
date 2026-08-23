---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: DoS of meta vault withdrawals during points phase if one vault is paused or
  attempted redemption exceeds the maximum
vuln_class: []
---

# DoS of meta vault withdrawals during points phase if one vault is paused or attempted redemption exceeds the maximum

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** `pUSDeVault::_withdraw` assumes any `USDe` shortfall is covered by the multi-vaults; however, `redeemRequiredBaseAssets()` does not guarantee that the required assets are available or actually withdrawn, so the subsequent ERC-20 token transfer could fail and DoS withdrawals if the ERC-4626 withdrawal does not already revert. Usage of `ERC4626Upgradeable::previewRedeem` in `redeemRequiredBaseAssets()` is problematic as this could attempt to withdraw more assets than the vault will allow. Per the [ERC-4626 specification](https://eips.ethereum.org/EIPS/eip-4626), `previewRedeem()`:
> * MUST NOT account for redemption limits like those returned from maxRedeem and should always act as though the redemption would be accepted, regardless if the user has enough shares, etc.
> * MUST NOT revert due to vault specific user/global limits. MAY revert due to other conditions that would also cause redeem to revert.

So an availability-aware check such as `maxWithdraw()` which considers pause states and any other limits should be used instead to prevent one vault reverting when it may be possible to process the withdrawal by redeeming from another.

**Impact:** If one of the supported meta vaults is paused or experiences a hack of the underlying `USDe` which results in a decrease in share price during the points phase then this will prevent withdrawals from being processed even if it is possible to do so by redeeming from another.

**Proof of Concept:** First modify the `MockERC4626` to simulate a vault that pauses deposits/withdrawals and could return fewer assets when querying `maxWithdraw()` when compared with `previewRedeem()`:

```solidity
contract MockERC4626 is ERC4626 {
    bool public depositsEnabled;
    bool public withdrawalsEnabled;
    bool public hacked;

    error DepositsDisabled();
    error WithdrawalsDisabled();

    event DepositsEnabled(bool enabled);
    event WithdrawalsEnabled(bool enabled);

    constructor(IERC20 token) ERC20("MockERC4626", "M4626") ERC4626(token)  {}

    function _deposit(address caller, address receiver, uint256 assets, uint256 shares) internal override {
        if (!depositsEnabled) {
            revert DepositsDisabled();
        }

        super._deposit(caller, receiver, assets, shares);
    }

    function _withdraw(address caller, address receiver, address owner, uint256 assets, uint256 shares)
        internal
        override
    {
        if (!withdrawalsEnabled) {
            revert WithdrawalsDisabled();
        }

        super._withdraw(caller, receiver, owner, assets, shares);
    }

    function maxWithdraw(address owner) public view override returns (uint256) {
        if (!withdrawalsEnabled) {
            revert WithdrawalsDisabled();
        }

        if (hacked) {
            return super.maxWithdraw(owner) / 2; // Reduce max withdraw by half to simulate some limit
        }
        return super.maxWithdraw(owner);
    }

    function totalAssets() public view override returns (uint256) {
        if (hacked) {
            return super.totalAssets() * 3/4; // Reduce total assets by 25% to simulate some loss
        }
        return super.totalAssets();
    }

    function setDepositsEnabled(bool depositsEnabled_) external {
        depositsEnabled = depositsEnabled_;
        emit DepositsEnabled(depositsEnabled_);
    }

    function setWithdrawalsEnabled(bool withdrawalsEnabled_) external {
        withdrawalsEnabled = withdrawalsEnabled_;
        emit WithdrawalsEnabled(withdrawalsEnabled_);
    }

    function hack() external {
        hacked = true;
    }
}
```

The following test can then be run in `pUSDeVault.t.sol`:
```solidity
error WithdrawalsDisabled();
error ERC4626ExceededMaxWithdraw(address owner, uint256 assets, uint256 max);
error ERC20InsufficientBalance(address from, uint256 balance, uint256 amount);

function test_redeemRequiredBaseAssetsDoS() public {
    assert(address(USDe) != address(0));

    account = msg.sender;

    // deposit USDe
    USDe.mint(account, 10 ether);
    deposit(USDe, 10 ether);
    assertBalance(pUSDe, account, 10 ether, "Initial deposit");

    // deposit eUSDe
    USDe.mint(account, 10 ether);
    USDe.approve(address(eUSDe), 10 ether);
    eUSDe.setDepositsEnabled(true);
    eUSDe.deposit(10 ether, account);
    assertBalance(eUSDe, account, 10 ether, "Deposit to eUSDe");
    eUSDe.approve(address(pUSDeDepositor), 10 ether);
    pUSDeDepositor.deposit(eUSDe, 10 ether, account);

    // simulate trying to withdraw from the eUSDe vault when it is paused
    uint256 withdrawAmount = 20 ether;
    eUSDe.setWithdrawalsEnabled(false);
    vm.expectRevert(abi.encodeWithSelector(WithdrawalsDisabled.selector));
    pUSDe.withdraw(address(USDe), withdrawAmount, account, account);
    eUSDe.setWithdrawalsEnabled(true);


    // deposit USDe from another account
    account = address(0x1234);
    vm.startPrank(account);
    USDe.mint(account, 10 ether);
    USDe.approve(address(eUSDe), 10 ether);
    eUSDe.deposit(10 ether, account);
    assertBalance(eUSDe, account, 10 ether, "Deposit to eUSDe");
    eUSDe.approve(address(pUSDeDepositor), 10 ether);
    pUSDeDepositor.deposit(eUSDe, 10 ether, account);
    vm.stopPrank();
    account = msg.sender;
    vm.startPrank(account);

    // deposit eUSDe2
    USDe.mint(account, 5 ether);
    USDe.approve(address(eUSDe2), 5 ether);
    eUSDe2.setDepositsEnabled(true);
    eUSDe2.deposit(5 ether, account);
    assertBalance(eUSDe2, account, 5 ether, "Deposit to eUSDe2");
    eUSDe2.approve(address(pUSDeDepositor), 5 ether);
    pUSDeDepositor.deposit(eUSDe2, 5 ether, account);


    // simulate when previewRedeem() in redeemRequiredBaseAssets() returns more than maxWithdraw() during withdrawal
    // as a result of a hack and imposition of a limit
    eUSDe.hack();
    uint256 maxWithdraw = eUSDe.maxWithdraw(address(pUSDe));
    vm.expectRevert(abi.encodeWithSelector(ERC4626ExceededMaxWithdraw.selector, address(pUSDe), withdrawAmount/2, maxWithdraw));
    pUSDe.withdraw(address(USDe), withdrawAmount, account, account);

    // attempt to withdraw from eUSDe2 vault, but redeemRequiredBaseAssets() skips withdrawal attempt
    // so there are insufficient assets to cover the subsequent transfer even though there is enough in the vaults
    eUSDe2.setWithdrawalsEnabled(true);
    vm.expectRevert(abi.encodeWithSelector(ERC20InsufficientBalance.selector, address(pUSDe), eUSDe2.balanceOf(address(pUSDe)), withdrawAmount));
    pUSDe.withdraw(address(eUSDe2), withdrawAmount, account, account);
}
```

**Recommended Mitigation:**
```diff
    function redeemRequiredBaseAssets (uint baseTokens) internal {
        for (uint i = 0; i < assetsArr.length; i++) {
            IERC4626 vault = IERC4626(assetsArr[i].asset);
--          uint totalBaseTokens = vault.previewRedeem(vault.balanceOf(address(this)));
++          uint256 totalBaseTokens = vault.maxWithdraw(address(this));
            if (totalBaseTokens >= baseTokens) {
                vault.withdraw(baseTokens, address(this), address(this));
                break;
            }
        }
    }
```

**Strata:** Fixed in commit [4efba0c](https://github.com/Strata-Money/contracts/commit/4efba0c484a3bd6d4934e0f1ec0eb91848c94298).

**Cyfrin:** Verified.
