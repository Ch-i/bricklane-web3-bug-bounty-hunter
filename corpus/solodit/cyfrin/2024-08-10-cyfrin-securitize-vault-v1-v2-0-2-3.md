---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-10-cyfrin-securitize-vault-v1-v2-0-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-10-cyfrin-securitize-vault-v1-v2-0
title: General notes on the design
vuln_class: []
---

# General notes on the design

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-10-cyfrin-securitize-vault-v1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md)_

---

**Description:**
1. In general, it is not clear why the team inherited ERC4626 vault.
The main point of using an ERC-4626 vault is to provide a standardized interface for managing "yield-bearing" tokenized vaults, enabling consistent tracking and calculation of share prices (i.e., the value of vault shares relative to the underlying assets).
But the `SecuritizeVault` enforces 1:1 ratio between the share and the asset, it voids the main point.
Furthermore, the vault has a function `liquidate()` that is not in the ERC4626 standard and it could confuse users and engineers because the term `liquidate` is used in lending protocols.
The current implementation does not show any clear evidence of necessity of using ERC4626.
It could be an overkill and also error prone.

2. The current implementaion has `impairedAssetBalance` and `impairedVaultBalance` and each of them has its relevant transfer functions. It is not clear why these are necessary. Based on the context given by the team during the call, we think these are introduced to swipe the redundant assets or shares that are sent to the vault contract "by mistake". In general, it is not a big concern for the protocol itself because it is after all the caller's mistake and that is not the protocol's responsibility. If the protocol is really concerned with the user mistakes, it is enough to have a single admin function. (refer to [Compound's sweep function](https://github.com/compound-finance/compound-protocol/blob/a3214f67b73310d547e00fc578e8355911c9d376/contracts/CErc20.sol#L124) below.) Note that the current implementation also consumes unnecessary gas because the internal function `_validateBalance()` is called for every transaction.
```solidity
    /**
     * @notice A public function to sweep accidental ERC-20 transfers to this contract. Tokens are sent to admin (timelock)
     * @param token The address of the ERC-20 token to sweep
     */
    function sweepToken(EIP20NonStandardInterface token) override external {
        require(msg.sender == admin, "CErc20::sweepToken: only admin can sweep tokens");
        require(address(token) != underlying, "CErc20::sweepToken: can not sweep underlying token");
        uint256 balance = token.balanceOf(address(this));
        token.transfer(admin, balance);
    }
```


**Securitize:** We chose to implement the `ERC-4626` standard over a `wrapped ERC-20` due to our future plans to implement a variable Net Asset Value (NAV) price. This means that the share-to-asset ratio will vary, making `ERC-4626’s` standardized interface for managing yield-bearing tokenized vaults beneficial. For the current use case, we are enforcing a 1:1 ratio, but this will change as we evolve our implementation.

Regarding the `liquidate()` function, it was included to meet the specific needs of our integration with lending protocols which will be the primary destination for the szTokens. The `liquidate()` method facilitates the process of converting `szTokens` to USDC. While we acknowledge that this function is not part of the `ERC-4626` standard and might cause some confusion, it is essential for our intended functionality. Additionally, not all users will be able to redeem their `szTokens` for a `DS Token`, so the only exit for them will be the liquidation method.

We removed the `_validateBalance()` and modified the impiarment methods:

```solidity
    /**
     * @dev Checks if the vault's asset balance impairment.
     *
     * @return uint256 Returns true if the asset balance is impaired, false otherwise.
     */
    function assetImpairedBalance() public view returns (uint256) {
        uint256 assetBalance = IERC20(asset()).balanceOf(address(this));
        uint256 impairedAssetBalance;
        if (assetBalance > totalSupply()) {
            impairedAssetBalance = assetBalance - totalSupply();
        }
        return impairedAssetBalance;
    }

    /**
     * @dev Checks if the vault's balance imparement.
     *
     * @return uint256 Returns the impaired vault balance.
     */
    function vaultImpairedBalance() public view returns (uint256) {
        uint256 impairedVaultBalance;
        if (balanceOf(address(this)) > 0) {
            impairedVaultBalance = balanceOf(address(this));
        }
        return impairedVaultBalance;
    }
```
Now this is a view, so the calculation will be on demand and gas free.
The need to extract the wrongly deposited tokens, is because of the DS Token is a regulated token, and we need to have an error fix mechanism. When an error occurs we need to have the consistency 1:1 ratio. If a szToken is locked, then the DS Token will be also locked.  Compound's sweep method as-is is not suitable, and also is very similar to the `transferImpairedXbalance` methods.
For the current model, the vault will have a specific owner-admin, and the owner-admin will be able to fix the error on demand.
```solidity
    /**
     * @dev Transfers the impaired asset balance to a specified address.
     * This method is used when the asset balance of the vault is considered impaired,
     * meaning it does not reflect the expected balance due to incorrect transfers into the vault.
     * Only callable by an account with the DEFAULT_ADMIN_ROLE.
     *
     * Requirements:
     * - The `assetIsImpaired()` function must return a value greater than 0.
     *
     * @param _to The address to which the impaired asset balance will be transferred.
     */
    function transferImpairedAssetBalance(address _to) external addressNotZero(_to) onlyRole(DEFAULT_ADMIN_ROLE) {
        uint256 _assetImpairedBalance = assetImpairedBalance();
        require(_assetImpairedBalance>0, "Asset balance is not impaired");
        IERC20 assetToken = IERC20(asset());
        assetToken.safeTransfer(_to, _assetImpairedBalance);
    }

    /**
     * @dev Transfers the impaired vault balance to a specified address.
     * This method is used when the vault's balance is considered impaired,
     * meaning it does not reflect the expected balance due to incorrect transfers out of the vault.
     * Only callable by an account with the DEFAULT_ADMIN_ROLE.
     *
     * Requirements:
     * - The `vaultImpairedBalance()` function must be return a value greater than 0.
     *
     * @param _to The address to which the impaired vault balance will be transferred.
     */
    function transferImpairedVaultBalance(address _to) external addressNotZero(_to) onlyRole(DEFAULT_ADMIN_ROLE) {
        uint _vaultImpairedBalance = vaultImpairedBalance();
        require(_vaultImpairedBalance>0, "Vault balance is not impaired");
        IERC20(address(this)).safeTransfer(_to, _vaultImpairedBalance);
    }
```

**Cyfrin:** Acknowledged.

\clearpage
