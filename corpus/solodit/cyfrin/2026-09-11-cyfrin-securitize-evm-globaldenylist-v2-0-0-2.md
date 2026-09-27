---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-0-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: Global denylist can be wired into compliance types that never check it
vuln_class: []
---

# Global denylist can be wired into compliance types that never check it

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** The `deploy-all` task takes `--compliance` and `--global-denylist-manager-address` as independent inputs. `getComplianceContractName` picks the compliance contract from the first one.

https://github.com/securitize-io/bc-global-denylist-manager-sc/blob/main/dstoken/tasks/utils/task.helper.ts#L19-L32

```ts
export const getComplianceContractName = (complianceType: string): string => {
  switch (complianceType) {
    case 'WHITELISTED':
      return 'ComplianceServiceWhitelisted';
    case 'GLOBAL_WHITELISTED':
      return 'ComplianceServiceGlobalWhitelisted';
    case 'BLACKLISTED':
    case 'PERMISSIONLESS':
      return 'ComplianceServicePermissionless';
    case 'REGULATED_MOCK':
      return 'ComplianceServiceRegulatedMock';
    default:
      return 'ComplianceServiceRegulated';
  }
}
```

`set-services` wires the denylist address into `dsToken` and `complianceService` whenever it is given, without looking at the compliance type.

https://github.com/securitize-io/bc-global-denylist-manager-sc/blob/main/dstoken/tasks/set-services.ts#L115-L119

```ts
if (globalDenylistManager) {
  console.log('Connecting compliance service to global denylist manager');
  tx = await complianceService.setDSService(DSConstants.services.GLOBAL_DENYLIST_MANAGER, globalDenylistManager.getAddress());
  await tx.wait();
}
```

Only `ComplianceServicePermissionless` calls `isGloballyDenylisted`. `ComplianceServiceWhitelisted`, `ComplianceServiceGlobalWhitelisted` and `ComplianceServiceRegulated` do not reference the `GLOBAL_DENYLIST_MANAGER` slot at all. The runbook only shows the flag with `--compliance PERMISSIONLESS`, but nothing enforces that.

**Impact:** A token deployed with any other compliance type and a denylist address reports a successful wiring, but the denylist is never consulted. A wallet on the global denylist can still be issued tokens and transfer them.

**Recommended Mitigation:** Fail the deploy task when the denylist address is supplied with a compliance type that does not enforce it.

https://github.com/securitize-io/bc-global-denylist-manager-sc/blob/main/dstoken/tasks/deploy-all.ts#L51-L57

```ts
const denylistCompliance = ['PERMISSIONLESS', 'BLACKLISTED'];
if (args.globalDenylistManagerAddress && !denylistCompliance.includes(args.compliance)) {
  throw new Error(
    `--global-denylist-manager-address is only supported with --compliance PERMISSIONLESS or BLACKLISTED, got ${args.compliance}`
  );
}
```

**Securitize:** Fixed in commit [db15596](https://github.com/securitize-io/dstoken/commit/db1559680419084cb3c91719492b03243d8e6353).

**Cyfrin:** Verified.
