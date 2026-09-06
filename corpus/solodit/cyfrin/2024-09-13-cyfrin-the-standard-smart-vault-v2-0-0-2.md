---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-0-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: '`USDs` self-backing breaks assumptions around economic peg-maintenance incentives'
vuln_class: []
---

# `USDs` self-backing breaks assumptions around economic peg-maintenance incentives

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** When `SmartVaultYieldManager::deposit` is called via `SmartVaultV4::depositYield`, [at least 10%](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L168) of the deposited collateral must be directed toward the `USDs` Hypervisor (which in turn holds an LP position in a protocol-managed `USDs/USDC` Ramses pool):

```solidity
function deposit(address _collateralToken, uint256 _usdPercentage) external returns (address _hypervisor0, address _hypervisor1) {
    if (_usdPercentage < MIN_USDS_PERCENTAGE) revert StablePoolPercentageError();
    uint256 _balance = IERC20(_collateralToken).balanceOf(address(msg.sender));
    IERC20(_collateralToken).safeTransferFrom(msg.sender, address(this), _balance);
    HypervisorData memory _hypervisorData = hypervisorData[_collateralToken];
    if (_hypervisorData.hypervisor == address(0)) revert HypervisorDataError();
    _usdDeposit(_collateralToken, _usdPercentage, _hypervisorData.pathToUSDC);
    /* snip: other hypervisor deposit */
}
```

When the value of the Smart Vault's collateral is determined by `SmartVaultV4::yieldVaultCollateral`, ignoring the issue of hardcoding stablecoins to $1, the value of the tokens underlying each Hypervisor is used:

```solidity
if (_token0 == address(USDs) || _token1 == address(USDs)) {
    // both USDs and its vault pair are € stablecoins, but can be equivalent to €1 in collateral
    _usds += _underlying0 * 10 ** (18 - ERC20(_token0).decimals());
    _usds += _underlying1 * 10 ** (18 - ERC20(_token1).decimals());
```

The issue for `USDs` Hypervisor deposits is that this [underlying balance](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L90-L93) of `USDs` counts toward the [total collateral value](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L113) of the Smart Vault, and there is no restriction on the maximum amount of collateral that can be directed toward this Hypervisor. Hence, users can use `USDs` to collateralize their `USDs` loans with up to as much as 100% of the total collateral deposited to the `USDs/USDC` pool (50% in `USDs` if both stablecoin tokens are assumed to be at peg).

**Impact:** Once the peg is lost for endogenously collateralized stablecoins, such as those backed by themselves, it becomes increasingly difficult to return to recover as the value of both the stablecoin and its collateral decrease in tandem. This self-backing also breaks the assumptions surrounding the economic incentives of the protocol intended to contribute to peg-maintenance.

**Recommended Mitigation:** Consider disallowing the use of `USDs` Hypervisor tokens as backing collateral and implementing some other mechanism to ensure sufficient liquidity in the pool. Alternatively, the percentage of collateral allowed to be directed toward the `USDs` Hypervisor could be limited, but this would not completely mitigate the risk.

**The Standard DAO:** Fixed by commit [`cc86606`](https://github.com/the-standard/smart-vault/commit/cc86606ef6f8c1fea84f378e7f324e648f9bcbc8).

**Cyfrin:** Verified, `USDs` no longer contributes to Smart Vault yield collateral.
