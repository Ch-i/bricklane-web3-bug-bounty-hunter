---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: Deploy task implicit `GlobalDenyListManager::initialize` resolution can silently
  deploy an uninitialized proxy
vuln_class: []
---

# Deploy task implicit `GlobalDenyListManager::initialize` resolution can silently deploy an uninitialized proxy

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** The `deploy-denylist-manager` task calls `hre.upgrades.deployProxy(GlobalDenyListManager, [])` with no explicit `initializer` option. In `@openzeppelin/hardhat-upgrades`, `getInitializerData` sets `allowNoInitialization = true` when the initializer option is omitted and the args array is empty - exactly this call. It then resolves a function named `initialize`; on a failed lookup it returns `0x` instead of throwing.

The lookup currently succeeds, so `GlobalDenyListManager::initialize` runs by delegatecall from the `ERC1967Proxy` constructor and deployment plus initialization are atomic. The deployer receives `DEFAULT_ADMIN_ROLE` in the same transaction that creates the proxy, leaving no front-running window. The finding is the fragility of that guarantee, not a live defect.

**Impact:** If `initialize` is renamed or replaced by a differently named initializer, the task deploys the proxy with empty init data and reports success. `initialize` is unauthenticated and grants `DEFAULT_ADMIN_ROLE` to `msg.sender`, and that role gates `BaseRBACContract::_authorizeUpgrade`, so the first caller of the uninitialized proxy gains full upgrade control. The test suite would not catch the regression: the upgrade test passes `initializer: 'initialize'` explicitly while the production task does not.

**Recommended Mitigation:** Name the initializer explicitly so a rename throws, and assert the post-deploy state:

```typescript
const denylistManager = await hre.upgrades.deployProxy(GlobalDenyListManager, [], {
  initializer: 'initialize',
});
await denylistManager.waitForDeployment();

const [deployer] = await hre.ethers.getSigners();
if ((await denylistManager.getInitializedVersion()) !== 1n) throw new Error('proxy not initialized');
if (!(await denylistManager.isAdmin(deployer.address))) throw new Error('deployer is not admin');
```

The explicit `initializer` option turns the silent skip into a thrown error, while `BaseRBACContract::getInitializedVersion` and `GlobalDenyListManager::isAdmin` assert the on-chain end state independently of plugin behavior.

**Securitize:** Fixed in commit [3e0e13a](https://github.com/securitize-io/bc-global-denylist-manager-sc/commit/3e0e13a72e685555cdf66f4e0726cb5a449dd947).

**Cyfrin:** Verified.
