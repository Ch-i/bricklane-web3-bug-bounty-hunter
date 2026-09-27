---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-1
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
title: '`deploy-full.ts` uses the wrong TIP-20 `renounceRole` signature'
vuln_class: []
---

# `deploy-full.ts` uses the wrong TIP-20 `renounceRole` signature

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** The deployment script declares and calls `renounceRole(bytes32,address)` on the native TIP-20. Tempo implements `renounceRole(bytes32)` instead ([TIP-20 specification](https://docs.tempo.xyz/protocol/tip20/spec)). Local tests use an OpenZeppelin-shaped mock and do not catch the mismatch.

**Impact:** Handover aborts after the incoming owner receives privileges but before the deployer divests, leaving two privileged accounts and an incomplete deployment.

**Proof of Concept:** Add the following test to `test/solace-pocs/NativeRenounceRoleAbi.test.ts`:

```typescript
import { expect } from "chai";
import { ethers } from "ethers";

const live = process.env.TEMPO_RPC ? describe : describe.skip;

live("Native TIP-20 renounceRole ABI", () => {
  const provider = new ethers.JsonRpcProvider(process.env.TEMPO_RPC as string);
  const PATH_USD = "0x20C0000000000000000000000000000000000000";
  const PROBE = "0x000000000000000000000000000000000000dEaD";
  const DEFAULT_ADMIN_ROLE = ethers.ZeroHash;
  const abi = ethers.AbiCoder.defaultAbiCoder();
  const UNKNOWN_SELECTOR = "0xaa4bc69a";
  const UNAUTHORIZED = "0x82b42900";

  async function classify(signature: string, types: string[], args: unknown[]) {
    const data = ethers.id(signature).slice(0, 10) + abi.encode(types, args).slice(2);
    try {
      await provider.call({ to: PATH_USD, data, from: PROBE });
      return "PRESENT";
    } catch (error: any) {
      const revertData = String(error.data ?? error.info?.error?.data ?? "");
      if (revertData.startsWith(UNKNOWN_SELECTOR)) return "ABSENT";
      if (revertData.startsWith(UNAUTHORIZED)) return "PRESENT";
      return `UNEXPECTED:${revertData.slice(0, 18)}`;
    }
  }

  it("rejects the two-argument signature used by the deployment script", async () => {
    expect(
      await classify(
        "renounceRole(bytes32,address)",
        ["bytes32", "address"],
        [DEFAULT_ADMIN_ROLE, PROBE]
      )
    ).to.equal("ABSENT");
  });

  it("implements the one-argument native signature", async () => {
    expect(
      await classify("renounceRole(bytes32)", ["bytes32"], [DEFAULT_ADMIN_ROLE])
    ).to.equal("PRESENT");
  });

  it("retains the expected signatures for the other role operations", async () => {
    const role = ethers.id("ISSUER_ROLE");
    expect(await classify("grantRole(bytes32,address)", ["bytes32", "address"], [role, PROBE])).to.equal("PRESENT");
    expect(await classify("revokeRole(bytes32,address)", ["bytes32", "address"], [role, PROBE])).to.equal("PRESENT");
    expect(await classify("setRoleAdmin(bytes32,bytes32)", ["bytes32", "bytes32"], [role, DEFAULT_ADMIN_ROLE])).to.equal("PRESENT");
    expect(await classify("hasRole(address,bytes32)", ["address", "bytes32"], [PROBE, role])).to.equal("PRESENT");
    expect(await classify("hasRole(bytes32,address)", ["bytes32", "address"], [role, PROBE])).to.equal("ABSENT");
  });
});
```

Run with: `TEMPO_RPC="https://your-tempo-mainnet-rpc" npx hardhat test test/solace-pocs/NativeRenounceRoleAbi.test.ts`

**Recommended Mitigation:** Use the one-argument ABI for the TIP-20 call while retaining the two-argument OpenZeppelin call for the registry and consumer. Source the native ABI from Tempo's SDK and verify every post-handoff role on a Tempo-compatible environment.

**Securitize:** Fixed in [PR 17](https://github.com/securitize-io/bc-tempo-sc/pull/17).

**Cyfrin:** Verified.
