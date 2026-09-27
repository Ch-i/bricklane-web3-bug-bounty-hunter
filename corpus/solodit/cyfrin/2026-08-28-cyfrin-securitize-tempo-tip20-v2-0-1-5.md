---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-5
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20TrustService::setServiceOwner` uses one-step ownership transfer'
vuln_class: []
---

# `Tip20TrustService::setServiceOwner` uses one-step ownership transfer

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20TrustService::setServiceOwner` immediately demotes the current `MASTER` and assigns the new address. The recipient does not accept the role, so an address typo or inaccessible account cannot be corrected afterward.

**Impact:** The stack can irreversibly lose abstract-role governance and upgrade authority for the trust and service-consumer proxies. The separate token, registry, and consumer `DEFAULT_ADMIN_ROLE` assignments are not transferred by this function and remain a distinct operational handoff concern.

**Proof of Concept:** Add the following test to `test/solace-pocs/OneStepServiceOwnerTransfer.test.ts`:

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-network-helpers";

const NONE = 0n;
const MASTER = 1n;
const ISSUER_ROLE = ethers.keccak256(ethers.toUtf8Bytes("ISSUER_ROLE"));
const PAUSE_ROLE = ethers.keccak256(ethers.toUtf8Bytes("PAUSE_ROLE"));
const UNPAUSE_ROLE = ethers.keccak256(ethers.toUtf8Bytes("UNPAUSE_ROLE"));
const BURN_BLOCKED_ROLE = ethers.keccak256(ethers.toUtf8Bytes("BURN_BLOCKED_ROLE"));
const REGISTRAR_ROLE = ethers.keccak256(ethers.toUtf8Bytes("REGISTRAR_ROLE"));
const LOCK_MANAGER_ROLE = ethers.keccak256(ethers.toUtf8Bytes("LOCK_MANAGER_ROLE"));
const ROLE_MANAGER_ROLE = ethers.keccak256(ethers.toUtf8Bytes("ROLE_MANAGER_ROLE"));

async function fixture() {
  const [admin, master, replacement] = await ethers.getSigners();
  const inaccessibleOwner = ethers.Wallet.createRandom().address;
  const tip403 = await ethers.deployContract("MockTIP403");
  const token: any = await ethers.deployContract("MockTIP20", [admin.address]);

  const Registry = await ethers.getContractFactory("Tip20RegistryService");
  const registryImplementation = await Registry.deploy();
  const registryProxy = await ethers.deployContract("ERC1967Proxy", [
    await registryImplementation.getAddress(),
    Registry.interface.encodeFunctionData("initialize", [admin.address, await tip403.getAddress()]),
  ]);
  const registry: any = Registry.attach(await registryProxy.getAddress());

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

  return { trust, master, replacement, inaccessibleOwner };
}

describe("One-step service-owner transfer", () => {
  it("irreversibly demotes the current MASTER before recipient acceptance", async () => {
    const { trust, master, replacement, inaccessibleOwner } = await loadFixture(fixture);

    expect(await trust.getRole(master.address)).to.equal(MASTER);
    await trust.connect(master).setServiceOwner(inaccessibleOwner);

    expect(await trust.getRole(master.address)).to.equal(NONE);
    expect(await trust.getRole(inaccessibleOwner)).to.equal(MASTER);
    await expect(
      trust.connect(master).setServiceOwner(replacement.address)
    ).to.be.revertedWithCustomError(trust, "InsufficientRole");
  });
});
```

Run with: `npx hardhat test test/solace-pocs/OneStepServiceOwnerTransfer.test.ts`

**Recommended Mitigation:** Use a two-step `pendingOwner` and acceptance flow. Keep the current `MASTER` active until the proposed owner accepts, and apply the protocol-address target checks before nomination.

**Securitize:** Fixed in [PR 16](https://github.com/securitize-io/bc-tempo-sc/pull/16/commits).

**Cyfrin:** Verified.
