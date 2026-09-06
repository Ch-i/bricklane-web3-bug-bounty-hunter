---
affected_contracts: []
derives_from: []
id: solodit-0x52-2025-05-02-hyperstable-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
tags:
- firm:0x52
- report:2025-05-02-hyperstable
title: '[M-01] `PositionManager#liquidatePosition` fails to update vaultDebt and vaultCollateral'
vuln_class: []
---

# [M-01] `PositionManager#liquidatePosition` fails to update vaultDebt and vaultCollateral

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2025-05-02-Hyperstable.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md)_

---

**Details**

**First discovered by Dev team during audit period**

[PositionManager.sol#L169-L185](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/core/PositionManager.sol#L169-L185)

        function liquidatePosition(address _vault, address _target, uint256 _debtToRepay, uint256 _sharesToLiquidate)
            external
        {
            if (msg.sender != liquidationManager) {
                revert OnlyLiquidatorManager();
            }
            // Debt and collateral shares are adjusted for the liquidated account
            _debtSnapshot[_target][_vault] -= _debtToRepay;
            collateralShares[_target][_vault] -= _sharesToLiquidate;


    @>      uint256 updatedVaultDebt = _vaultDebtSnapshot[_vault] - _debtToRepay;
    @>      uint256 updatedVaultCollateral = vaultCollateral[_vault] - _sharesToLiquidate;


            interestRateStrategy.updateVaultInterestRate(
                _vault, updatedVaultCollateral.mulWad(IVault(_vault).sharePrice()), updatedVaultDebt, IVault(_vault).MCR()
            );
        }

In the above lines we see that `_vaultDebtSnapshot` and `vaultCollateral` are not update when performing the liquidation. This leaves phantom collateral and debt in the system which can lead to inaccurate interest rates.

**Lines of Code**

[PositionManager.sol#L179-L180](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/core/PositionManager.sol#L179-L180)

**Recommendation**

`_vaultDebtSnapshot` and `vaultCollateral` should be updated

**Remediation**

Fixed in [1277f39](https://github.com/hyperstable/contracts/commit/1277f396dcd14f00c6258eb1f9668f43be1d311f). Updated values are now correctly written to storage.
