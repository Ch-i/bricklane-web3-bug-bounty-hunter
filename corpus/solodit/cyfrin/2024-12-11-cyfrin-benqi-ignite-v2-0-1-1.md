---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: The default admin role controls all other roles within `StakingContract`
vuln_class: []
---

# The default admin role controls all other roles within `StakingContract`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** Within `StakingContract`, there is intended separation between the Zeeve and BENQI admin/super-admin roles as implemented in the [`grantAdminRole()`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L986), [`revokeAdminRole()`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L1017), and [`updateAdminRole()`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L1048) functions. The intention is for admin roles to be managed by the corresponding super-admin; however, `AccessControlUpgradeable::_setRoleAdmin` is never invoked for any of the roles and the current implementation fails to consider the default admin role that is [granted to the BENQI super-admin](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L169) for pausing purposes when the contract is initialized. As a result, the BENQI super-admin can be used to manage all other roles by invoking `AccessControlUpgradeable::grantRole` and `AccessControlUpgradeable::revokeRole` directly. This behavior is used in `Ignite` and `ValidatorRewarder` to grant the appropriate roles; however, it is not desirable in `StakingContract`.

**Impact:** The default admin role granted to the BENQI super-admin can be used to control all other roles.

**Proof of Concept:** The following test can be added to `stakingContract.test.js` under `describe("updateAdminRole")`:

```javascript
it("allows BENQI_SUPER_ADMIN to update ZEEVE_SUPER_ADMIN", async function () {
    const zeeveSuperAdminRole = await stakingContract.ZEEVE_SUPER_ADMIN_ROLE();

    // BENQI_SUPER_ADMIN can use OpenZepplin's grantRole to alter ZEEVE_SUPER_ADMIN_ROLE
    await stakingContract.connect(benqiSuperAdmin).grantRole(zeeveSuperAdminRole, otherUser.address);
    await stakingContract.connect(benqiSuperAdmin).revokeRole(zeeveSuperAdminRole, zeeveSuperAdmin.address);

    expect(await stakingContract.hasRole(zeeveSuperAdminRole, otherUser.address)).to.be.true;
    expect(await stakingContract.hasRole(zeeveSuperAdminRole, zeeveSuperAdmin.address)).to.be.false;
});
```

An equivalent Foundry test can be run with the provided fixtures:

```solidity
function test_defaultAdminControlsAllRolesPoC() public {
    assertEq(stakingContract.getRoleAdmin(stakingContract.DEFAULT_ADMIN_ROLE()), stakingContract.DEFAULT_ADMIN_ROLE());
    assertEq(stakingContract.getRoleAdmin(stakingContract.BENQI_SUPER_ADMIN_ROLE()), stakingContract.DEFAULT_ADMIN_ROLE());
    assertEq(stakingContract.getRoleAdmin(stakingContract.BENQI_ADMIN_ROLE()), stakingContract.DEFAULT_ADMIN_ROLE());
    assertEq(stakingContract.getRoleAdmin(stakingContract.ZEEVE_SUPER_ADMIN_ROLE()), stakingContract.DEFAULT_ADMIN_ROLE());
    assertEq(stakingContract.getRoleAdmin(stakingContract.ZEEVE_ADMIN_ROLE()), stakingContract.DEFAULT_ADMIN_ROLE());

    address EXTERNAL_ADDRESS = makeAddr("EXTERNAL_ADDRESS");
    vm.startPrank(BENQI_SUPER_ADMIN);
    stakingContract.grantRole(stakingContract.ZEEVE_SUPER_ADMIN_ROLE(), EXTERNAL_ADDRESS);
    vm.stopPrank();
    assertTrue(stakingContract.hasRole(stakingContract.ZEEVE_SUPER_ADMIN_ROLE(), EXTERNAL_ADDRESS));
}
```

**Recommended Mitigation:** Consider either:
1. Setting the appropriate role admins during initialization.
2. Removing the default admin role and creating a separate pauser role.
3. Overriding the OpenZeppelin functions to prevent them from being called directly.

**BENQI:** Fixed in commit [491a278](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/491a278be80605bbf23cef71bed5227ea11d201e).

**Cyfrin:** Verified. The OpenZeppelin function have been overridden.
