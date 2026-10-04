---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20RegistryService::policyId` can drift from the token transfer policy'
vuln_class: []
---

# `Tip20RegistryService::policyId` can drift from the token transfer policy

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20RegistryService::policyId` is immutable after setup, but the token administrator can change the token's effective policy. Registry writes and `isAuthorized` then use the old policy. Since Tempo T9, the effective token binding can be queried through TIP-403 `tokenTransferPolicyId` ([TIP-1092](https://github.com/tempoxyz/tempo/blob/main/tips/tip-1092.md)).

**Impact:** After a privileged policy rotation, registry state can diverge from the policy that actually gates transfers. Compliance operations may update an inactive policy until the stack is upgraded or reconfigured.

**Proof of Concept:** Add the following test to `test/solace-pocs/PolicyBindingDrift.test.ts`:

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-network-helpers";

const REGISTRY_POLICY = 2n;
const ROTATED_TOKEN_POLICY = 3n;

async function fixture() {
  const [admin, registrar, lockManager, wallet] = await ethers.getSigners();
  const tip403 = await ethers.deployContract("MockTIP403");
  const Registry = await ethers.getContractFactory("Tip20RegistryService");
  const implementation = await Registry.deploy();
  const proxy = await ethers.deployContract("ERC1967Proxy", [
    await implementation.getAddress(),
    Registry.interface.encodeFunctionData("initialize", [admin.address, await tip403.getAddress()]),
  ]);
  const registry: any = Registry.attach(await proxy.getAddress());

  await registry.setPolicyId(REGISTRY_POLICY);
  await registry.grantRole(await registry.REGISTRAR_ROLE(), registrar.address);
  await registry.grantRole(await registry.LOCK_MANAGER_ROLE(), lockManager.address);
  await registry.connect(registrar).registerInvestor("INV-1");
  await registry.connect(registrar).addWallet(wallet.address, "INV-1");

  return { registry, tip403, lockManager, wallet };
}

describe("Registry and token policy binding drift", () => {
  it("records a lock only in the registry's stale policy", async () => {
    const { registry, tip403, lockManager, wallet } = await loadFixture(fixture);

    // Model an external privileged token rotation by making policy 3 the
    // policy that token enforcement reads, while the registry remains on 2
    await tip403.modifyPolicyWhitelist(ROTATED_TOKEN_POLICY, wallet.address, true);

    await registry.connect(lockManager).lockInvestor("INV-1");

    expect(await registry.isInvestorLocked("INV-1")).to.equal(true);
    expect(await tip403.isAuthorized(REGISTRY_POLICY, wallet.address)).to.equal(false);
    expect(await tip403.isAuthorized(ROTATED_TOKEN_POLICY, wallet.address)).to.equal(true);
    await expect(registry.setPolicyId(ROTATED_TOKEN_POLICY)).to.be.revertedWithCustomError(
      registry,
      "PolicyIdAlreadySet"
    );
  });
});
```

Run with: `npx hardhat test test/solace-pocs/PolicyBindingDrift.test.ts`

The test models the out-of-scope privileged token rotation by treating policy 3 as the policy read by token enforcement while the registry remains bound to policy 2.

**Recommended Mitigation:** Resolve the token address and compare its effective TIP-403 binding before every policy mutation. Provide an owner-authorized upgrade or migration path that updates the registry binding only after verifying policy type and administration.

**Securitize:** Fixed in [PR 18](https://github.com/securitize-io/bc-tempo-sc/pull/18).

**Cyfrin:** Verified.
