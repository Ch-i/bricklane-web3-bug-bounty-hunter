---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-1-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Unauthorized role grants prevent `QuantAMMBaseAdministration` deployment
vuln_class: []
---

# Unauthorized role grants prevent `QuantAMMBaseAdministration` deployment

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** `QuantAMMBaseAdministration` is a contract that manages certain break-glass features and facilitates calls to other QuantAMM contracts.

However, this contract fails to deploy due to an issue in the [`QuantAMMBaseAdministration` constructor](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMBaseAdministration.sol#L68-L74), where roles are granted to proposers and executors:

```solidity
for (uint256 i = 0; i < proposers.length; i++) {
    timelock.grantRole(timelock.PROPOSER_ROLE(), proposers[i]);
}

for (uint256 i = 0; i < executors.length; i++) {
    timelock.grantRole(timelock.EXECUTOR_ROLE(), executors[i]);
}
```
The issue arises because the `QuantAMMBaseAdministration` contract needs to have the `DEFAULT_ADMIN_ROLE` in the `timelock` contract for these `grantRole` calls to succeed. Since it does not possess this role, the calls will [revert](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/access/AccessControl.sol#L122-L124) with an `AccessControlUnauthorizedAccount` error.

**Impact:** The deployment of `QuantAMMBaseAdministration` will fail due to unauthorized role assignment, preventing the contract from being deployed successfully.

**Proof of Concept:** Add the following test file to the `pkg/pool-quantamm/test/foundry/` folder:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "forge-std/Test.sol";
import "../../contracts/QuantAMMBaseAdministration.sol";

contract QuantAMMBaseAdministrationTest is Test {

    address daoRunner = makeAddr("daoRunner");

    address proposer = makeAddr("proposer");
    address executor = makeAddr("executor");

    QuantAMMBaseAdministration admin;

    function testSetupQuantAMMBaseAdministration() public {
        address[] memory proposers = new address[](1);
        proposers[0] = proposer;

        address[] memory executors = new address[](1);
        executors[0] = executor;

        vm.expectRevert(); // AccessControlUnauthorizedAccount(address(admin),DEFAULT_ADMIN_ROLE)
        admin = new QuantAMMBaseAdministration(
            daoRunner,
            1 hours,
            proposers,
            executors
        );
    }
}
```

**Recommended Mitigation:** Remove the role grants in the constructor, as these assignments are already handled in the `TimeLockController` [constructor]((https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/governance/TimelockController.sol#L125-L133)):

**QuantAMM:** Fixed in [`a299ce7`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/a299ce72076b58503386bc146b81014560536d9e)

**Cyfrin:** Verified. `QuantAMMBaseAdministration` is removed.

\clearpage
