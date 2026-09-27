---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20TrustService::_project` can revoke unmanaged native grants'
vuln_class: []
---

# `Tip20TrustService::_project` can revoke unmanaged native grants

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20TrustService::_project` revokes every native role in an outgoing abstract projection without knowing who granted it. A lateral role holder can assign and then remove an abstract role from an account that already held the same native permission directly, deleting the unmanaged grant.

**Impact:** A trust transition can unexpectedly remove break-glass or manually provisioned permissions. A `MASTER` can recover them, so this does not permanently seize governance.

**Proof of Concept:** Add the following test to `test/solace-pocs/UnmanagedNativeGrantRevocation.test.ts`:

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-network-helpers";

const NONE = 0;
const MASTER = 1;
const ISSUER = 2;
const REGISTRAR_ROLE = ethers.keccak256(ethers.toUtf8Bytes("REGISTRAR_ROLE"));
const LOCK_MANAGER_ROLE = ethers.keccak256(ethers.toUtf8Bytes("LOCK_MANAGER_ROLE"));
const ISSUER_ROLE = ethers.keccak256(ethers.toUtf8Bytes("ISSUER_ROLE"));
const PAUSE_ROLE = ethers.keccak256(ethers.toUtf8Bytes("PAUSE_ROLE"));
const UNPAUSE_ROLE = ethers.keccak256(ethers.toUtf8Bytes("UNPAUSE_ROLE"));
const BURN_BLOCKED_ROLE = ethers.keccak256(ethers.toUtf8Bytes("BURN_BLOCKED_ROLE"));
const ROLE_MANAGER_ROLE = ethers.keccak256(ethers.toUtf8Bytes("ROLE_MANAGER_ROLE"));

async function fixture() {
  const [admin, master, issuer, walletRegistrar] = await ethers.getSigners();
  const tip403 = await ethers.deployContract("MockTIP403");
  const token: any = await ethers.deployContract("MockTIP20", [admin.address]);

  const Registry = await ethers.getContractFactory("Tip20RegistryService");
  const registryImplementation = await Registry.deploy();
  const registryProxy = await ethers.deployContract("ERC1967Proxy", [
    await registryImplementation.getAddress(),
    Registry.interface.encodeFunctionData("initialize", [admin.address, await tip403.getAddress()]),
  ]);
  const registry: any = Registry.attach(await registryProxy.getAddress());
  await registry.grantRole(REGISTRAR_ROLE, walletRegistrar.address);

  const Trust = await ethers.getContractFactory("Tip20TrustService");
  const trustImplementation = await Trust.deploy();
  const trustProxy = await ethers.deployContract("ERC1967Proxy", [
    await trustImplementation.getAddress(),
    Trust.interface.encodeFunctionData("initialize", [
      master.address,
      await token.getAddress(),
      await registry.getAddress(),
    ]),
  ]);
  const trust: any = Trust.attach(await trustProxy.getAddress());
  const trustAddress = await trust.getAddress();

  for (const role of [ISSUER_ROLE, PAUSE_ROLE, UNPAUSE_ROLE, BURN_BLOCKED_ROLE]) {
    await token.setRoleAdmin(role, ROLE_MANAGER_ROLE);
  }
  await token.grantRole(ROLE_MANAGER_ROLE, trustAddress);
  await registry.setRoleAdmin(REGISTRAR_ROLE, ROLE_MANAGER_ROLE);
  await registry.setRoleAdmin(LOCK_MANAGER_ROLE, ROLE_MANAGER_ROLE);
  await registry.grantRole(ROLE_MANAGER_ROLE, trustAddress);
  await trust.connect(master).setRole(issuer.address, ISSUER);

  return { trust, registry, admin, master, issuer, walletRegistrar };
}

describe("Unmanaged native grant revocation", () => {
  it("lets an issuer erase a registrar grant that the trust did not create", async () => {
    const { trust, registry, issuer, walletRegistrar } = await loadFixture(fixture);

    expect(await registry.hasRole(REGISTRAR_ROLE, walletRegistrar.address)).to.equal(true);
    expect(await trust.getRole(walletRegistrar.address)).to.equal(NONE);
    expect(await trust.getRole(issuer.address)).to.equal(ISSUER);
    expect(await trust.getRole(issuer.address)).to.not.equal(MASTER);

    await trust.connect(issuer).setRole(walletRegistrar.address, ISSUER);
    await trust.connect(issuer).removeRole(walletRegistrar.address);

    expect(await registry.hasRole(REGISTRAR_ROLE, walletRegistrar.address)).to.equal(false);
  });

  it("prevents the token owner from restoring the grant directly", async () => {
    const { trust, registry, admin, master, walletRegistrar } = await loadFixture(fixture);

    await trust.connect(master).setRole(walletRegistrar.address, ISSUER);
    await trust.connect(master).removeRole(walletRegistrar.address);

    await expect(registry.connect(admin).grantRole(REGISTRAR_ROLE, walletRegistrar.address)).to.be.reverted;
  });
});
```

Run with: `npx hardhat test test/solace-pocs/UnmanagedNativeGrantRevocation.test.ts`

**Recommended Mitigation:** Treat direct native grants as an explicit break-glass state and reconcile them before trust transitions. If coexistence is required, track which grants the trust introduced and revoke only those grants, with tests for pre-existing native permissions.

**Securitize:** Acknowledged.
