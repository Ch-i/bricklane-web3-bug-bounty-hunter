---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[I-01] Deploying an Unlocker with Multicall may revert for 0 deposit amounts'
vuln_class: []
---

# [I-01] Deploying an Unlocker with Multicall may revert for 0 deposit amounts

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TTUMulticallDeployer.sol](https://github.com/EthSign/tokentable-v2-evm/tree/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/proxy/TTUMulticallDeployer.sol)

**Description:**

The `TTUMulticallDeployer` contracts allows projects to deploy an Unlocker, create presets, create actuals and deposit their project token in one call. A project may not want to deposit tokens into the Unlocker yet and desire to do it at a later stage (possibly after custom fees have been set up). However, if the project token reverts at 0 amount transfers, then the multicall will also revert:

```solidity
function multicallDeploy(
    ITTUDeployer deployer,
    bytes memory encodedDeployerParams,
    bytes calldata encodedCreatePresetsParams,
    bytes calldata encodedCreateActualsParams
) external {
    ITokenTableUnlockerV2 unlocker;
    {
        (
            address projectToken,
            address existingFutureToken,
            string memory projectId,
            bool isUpgradeable,
            bool isTransferable,
            bool isCancelable,
            bool isHookable,
            bool isWithdrawable,
            uint256 depositAmount
        ) = abi.decode(encodedDeployerParams, (address, address, string, bool, bool, bool, bool, bool, uint256));
        (unlocker,) = deployer.deployTTSuite(
            projectToken,
            existingFutureToken,
            projectId,
            isUpgradeable,
            isTransferable,
            isCancelable,
            isHookable,
            isWithdrawable
        );

        IERC20(projectToken).transferFrom(msg.sender, address(unlocker), depositAmount);
    }
    ...
}
```

**Impact:** Deploying with multicall will revert for 0 deposit amounts if the project token reverts for such transfers.

**Recommendation:** Implement a check that only call `transferFrom(...)` if the `depositAmount` is greater than 0.

**Status:** Acknowledged

**Update from TokenTable:** acknowledged
