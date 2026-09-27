---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-1-5
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: '`deploy-all` treats a zero `--global-denylist-manager-address` as wired, logging
  success while leaving global denylist enforcement off'
vuln_class: []
---

# `deploy-all` treats a zero `--global-denylist-manager-address` as wired, logging success while leaving global denylist enforcement off

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `deploy-all` declares `--global-denylist-manager-address` as an optional string parameter defaulting to `undefined`, and guards the wiring branch with a bare truthiness test. The zero address arrives as the non-empty 42-character string `0x0000000000000000000000000000000000000000`, which is truthy in JavaScript, so passing it selects the wired branch.

That branch logs that an existing manager is being used, then resolves the address with `ethers.getContractAt`, which never queries the chain for code. `set-services` subsequently takes both of its own guarded branches, logging one connection line for the token and another for the compliance service while writing `address(0)` into both `GLOBAL_DENYLIST_MANAGER` slots.

The resulting on-chain state is an unset slot, which is precisely the fail-open branch in `ComplianceServicePermissionless::_isGloballyDenylisted`. The token ends up with no global denylist enforcement while three separate log lines state that the manager was wired.

**Impact:** Omitting the flag and passing the zero address produce identical on-chain state but opposite operator-visible evidence. Omission is silent: the guard is skipped and the deploy log never mentions the global denylist at all. The zero address is actively misleading: the log asserts success three times.

**Recommended Mitigation:** Reject the zero address explicitly, and make the omitted case visible:

```typescript
if (args.globalDenylistManagerAddress) {
  if (args.globalDenylistManagerAddress === ethers.ZeroAddress) {
    throw new Error('--global-denylist-manager-address cannot be the zero address; omit the flag to deploy unwired');
  }
  console.log(`Using existing shared Global Denylist Manager at: ${args.globalDenylistManagerAddress}`);
  globalDenylistManager = await ethers.getContractAt('IDSGlobalDenyListManager', args.globalDenylistManagerAddress);
} else {
  console.log('WARNING: GLOBAL_DENYLIST_MANAGER left unset - global denylist enforcement is OFF for this token');
}
```

The `else` branch carries as much value as the guard itself: it turns the silent omission into a visible one, so neither path can leave an operator believing enforcement is active when it is not. Aligning both repositories on a single convention for an unset address parameter would remove the underlying inconsistency rather than only its symptom here.

**Securitize:** Fixed in commit [cbfcd9e](https://github.com/securitize-io/dstoken/commit/cbfcd9e332f8f81522c0cd709be16b3eef8e496e).

**Cyfrin:** Verified.
