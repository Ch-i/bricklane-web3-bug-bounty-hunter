---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: Precision loss causes systematic under-reporting of voting power for high decimal
  tokens
vuln_class: []
---

# Precision loss causes systematic under-reporting of voting power for high decimal tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** The `NormalizedTokenDecimalsVPCalc::_normalizeVaultTokenDecimals()`  causes voting power loss for legitimate stakeholders when high-decimal tokens (>24 decimals) are used. This occurs due to integer division in the Scaler.scale() function, which rounds down small results to zero.

```solidity
// NormalizedTokenDecimalsVPCalc.sol
function _normalizeVaultTokenDecimals(address vault, uint256 votingPower) internal view virtual returns (uint256) {
    return votingPower.scale(IERC20Metadata(_getCollateral(vault)).decimals(), BASE_DECIMALS); //@audit BASE_DECIMALS = 24
}

//Scaler.sol
function scale(uint256 value, uint8 decimals, uint8 targetDecimals) internal pure returns (uint256) {
    if (decimals > targetDecimals) {
        uint256 decimalsDiff;
        unchecked {
            decimalsDiff = decimals - targetDecimals;
        }
        return value / 10 ** decimalsDiff;  // @audit precision loss
    }
    // ...
}
```
When decimals > BASE_DECIMALS (24), the function divides by 10^(decimals-24), causing stakes smaller than this divisor to become zero voting power.

```text
// Divisor = 10^(30-24) = 10^6 = 1,000,000
Stake: 999,999 units → Voting Power: 0
Stake: 500,000 units → Voting Power: 0
Stake: 1,000,000 units → Voting Power: 1
```

All voting power calculators that extend `NormalizedTokenDecimalsVPCalc` are affected.

**Impact:** Legitimate stakeholders with meaningful economic stakes can lose voting power.

**Proof of Concept:** Add this to `NormalizedTokenDecimalsVPCalc.t.sol`

```solidity
function test_PrecisionLossPoC_30Decimals() public {
    // Even worse case with 30 decimals
    votingPowerProvider =
        new TestVotingPowerProvider(address(symbioticCore.operatorRegistry), address(symbioticCore.vaultFactory));

    INetworkManager.NetworkManagerInitParams memory netInit =
        INetworkManager.NetworkManagerInitParams({network: vars.network.addr, subnetworkID: IDENTIFIER});

    // Create token with 30 decimals (6 more than BASE_DECIMALS=24)
    MockToken mockToken = new MockToken("MockToken", "MTK", 30);

    IVotingPowerProvider.VotingPowerProviderInitParams memory votingPowerProviderInit = IVotingPowerProvider
        .VotingPowerProviderInitParams({
        networkManagerInitParams: netInit,
        ozEip712InitParams: IOzEIP712.OzEIP712InitParams({name: "MyVotingPowerProvider", version: "1"}),
        slashingWindow: 100,
        token: address(mockToken)
    });

    votingPowerProvider.initialize(votingPowerProviderInit);
    _networkSetMiddleware_SymbioticCore(vars.network.addr, address(votingPowerProvider));

    // Demonstrate extreme precision loss
    // Divisor = 10^(30-24) = 10^6 = 1,000,000

    Vm.Wallet memory operator = getOperator(0);
    vm.startPrank(operator.addr);
    votingPowerProvider.registerOperator(operator.addr);
    vm.stopPrank();

    address operatorVault = _getVault_SymbioticCore(
        VaultParams({
            owner: operator.addr,
            collateral: address(mockToken),
            burner: 0x000000000000000000000000000000000000dEaD,
            epochDuration: votingPowerProvider.getSlashingWindow() * 2,
            whitelistedDepositors: new address[](0),
            depositLimit: 0,
            delegatorIndex: 2,
            hook: address(0),
            network: address(0),
            withSlasher: true,
            slasherIndex: 0,
            vetoDuration: 1
        })
    );

    _operatorOptIn_SymbioticCore(operator.addr, operatorVault);
    _networkSetMaxNetworkLimit_SymbioticCore(
        votingPowerProvider.NETWORK(),
        operatorVault,
        votingPowerProvider.SUBNETWORK_IDENTIFIER(),
        type(uint256).max
    );
    _curatorSetNetworkLimit_SymbioticCore(
        operator.addr, operatorVault, votingPowerProvider.SUBNETWORK(), type(uint256).max
    );

    _deal_Symbiotic(address(mockToken), getStaker(0).addr, type(uint128).max, true);

    // Deposit 999,999 units - substantial economic value but < 1,000,000 divisor
    _stakerDeposit_SymbioticCore(getStaker(0).addr, operatorVault, 999_999);

    vm.startPrank(vars.network.addr);
    votingPowerProvider.registerOperatorVault(operator.addr, operatorVault);
    vm.stopPrank();

    address[] memory operatorVaults = votingPowerProvider.getOperatorVaults(operator.addr);
    uint256 actualVotingPower = votingPowerProvider.getOperatorVotingPower(operator.addr, operatorVaults[0], "");

    console.log("30-decimal token test:");
    console.log("  Stake: 999,999 units (substantial economic value)");
    console.log("  Divisor: 1,000,000 (10^6)");
    console.log("  Actual Voting Power: %d", actualVotingPower);
    console.log("  This demonstrates COMPLETE voting power loss for legitimate stakeholders!");

    // This will fail, demonstrating the precision loss
    assertEq(actualVotingPower, 0, "Voting power is 0 due to precision loss - this is the BUG!");
}
```

**Recommended Mitigation:** Consider restricting tokens with > 24 decimals. Alternatively, revise the `_normalizeVaultTokenDecimals` to ensure non-zero stakes get minimum 1 voting power:

```solidity
function _normalizeVaultTokenDecimals(address vault, uint256 votingPower) internal view virtual returns (uint256) {
    uint8 tokenDecimals = IERC20Metadata(_getCollateral(vault)).decimals();

    if (tokenDecimals > BASE_DECIMALS) {
        uint256 scaled = votingPower.scale(tokenDecimals, BASE_DECIMALS);
        return (scaled == 0 && votingPower > 0) ? 1 : scaled; //@audit give minimum voting power
    }

    return votingPower.scale(tokenDecimals, BASE_DECIMALS);
}
```


**Symbiotic:** Acknowledged.

**Cyfrin:** Acknowledged.
