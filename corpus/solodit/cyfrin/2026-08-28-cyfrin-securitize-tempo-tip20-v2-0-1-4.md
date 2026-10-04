---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-4
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
title: '`Tip20RegistryService::setPolicyId` accepts built-in TIP-403 policies'
vuln_class: []
---

# `Tip20RegistryService::setPolicyId` accepts built-in TIP-403 policies

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20RegistryService::setPolicyId` accepts policy 0 and policy 1. TIP-403 defines them as always-reject and always-allow, while custom policies start at 2 ([TIP-403 specification](https://docs.tempo.xyz/protocol/tip403/spec)). Before configuration, `Tip20RegistryService::isAuthorized` also queries policy 0 without checking `_policyIdSet`.

**Impact:** A one-shot configuration with policy 0 blocks all transfers; policy 1 makes registry whitelist changes ineffective. The registry cannot correct the binding without an upgrade.

**Proof of Concept:** Add the following test to `test/solace-pocs/BuiltinPolicyBinding.test.ts`:

```typescript
import { expect } from "chai";
import { ethers } from "ethers";

const live = process.env.TEMPO_RPC ? describe : describe.skip;

live("TIP-403 built-in policy binding", () => {
  const provider = new ethers.JsonRpcProvider(process.env.TEMPO_RPC as string);
  const TIP403 = "0x403c000000000000000000000000000000000000";
  const abi = ethers.AbiCoder.defaultAbiCoder();
  const sampleAddresses = [
    "0x000000000000000000000000000000000000dEaD",
    "0x1111111111111111111111111111111111111111",
    "0x251d2711ebeB0a09fdB8992F5506f3D949175246",
  ];

  const call = async (signature: string, types: string[], args: unknown[]) =>
    provider.call({
      to: TIP403,
      data: ethers.id(signature).slice(0, 10) + abi.encode(types, args).slice(2),
    });

  const isAuthorized = async (policyId: number, account: string) =>
    BigInt(
      await call("isAuthorized(uint64,address)", ["uint64", "address"], [policyId, account])
    ) === 1n;

  it("always rejects under policy 0 and always allows under policy 1", async () => {
    for (const account of sampleAddresses) {
      expect(await isAuthorized(0, account)).to.equal(false);
      expect(await isAuthorized(1, account)).to.equal(true);
    }
  });

  it("reports the zero address as administrator of both built-in policies", async () => {
    for (const policyId of [0, 1]) {
      const [, admin] = abi.decode(
        ["uint8", "address"],
        await call("policyData(uint64)", ["uint64"], [policyId])
      );
      expect(admin).to.equal(ethers.ZeroAddress);
    }
  });

  it("reserves custom policy IDs above the built-ins", async () => {
    const nextPolicyId = BigInt(await call("policyIdCounter()", [], []));
    expect(nextPolicyId).to.be.greaterThan(1n);
  });
});
```

Run with: `TEMPO_RPC="https://your-tempo-mainnet-rpc" npx hardhat test test/solace-pocs/BuiltinPolicyBinding.test.ts`

**Recommended Mitigation:** Require a custom policy ID, verify that it exists, is a whitelist, and is administered by the registry. Make `isAuthorized` revert or return an explicit unconfigured result until the binding is set.

**Securitize:** Fixed in [PR 15](https://github.com/securitize-io/bc-tempo-sc/pull/15).

**Cyfrin:** Verified.
