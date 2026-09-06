---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`Yield_Util::callDistributeYield` batches all assets in one unbounded loop,
  so one reverting vault blocks all yield'
vuln_class: []
---

# `Yield_Util::callDistributeYield` batches all assets in one unbounded loop, so one reverting vault blocks all yield

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `Yield_Util::callDistributeYield` (`stbl-contracts-evm-redemptions/contracts/Util.sol:69-83`) distributes yield by iterating every registered asset and calling `distributeYield()` on each vault in a single transaction:

```solidity
function callDistributeYield() external {
    if (!_registry.hasRole(YIELD_DISTRIBUTION_ROLE, msg.sender))
        revert Unauthorized_Caller(msg.sender);

    uint256 count = _registry.fetchCounter();

    for (uint256 i = 1; i <= count; i++) {
        AssetDefinition memory asset = _registry.fetchAssetData(i);

        if (asset.status != AssetStatus.ENABLED) continue;
        if (asset.vault == address(0)) continue;

        iSTBL_T1_Vault(asset.vault).distributeYield();
    }
}
```

The loop has no per-vault error isolation (no `try/catch`) and no upper bound. If any one vault's `distributeYield()` reverts (a paused vault, a transient oracle or price failure, a misconfigured or malicious vault), the whole batch reverts and no asset receives its distribution. As the asset registry grows, the same unbounded loop eventually exceeds the block gas limit.

**Impact:** DoS

**Recommended Mitigation:** Isolate per-vault failures, and provide a per-asset distribution entrypoint:

```solidity
for (uint256 i = 1; i <= count; i++) {
    AssetDefinition memory asset = _registry.fetchAssetData(i);
    if (asset.status != AssetStatus.ENABLED || asset.vault == address(0)) continue;
    try iSTBL_T1_Vault(asset.vault).distributeYield() {} catch {}
}
```

**STBL:** Fixed in commit [28f2868](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/28f2868037b0a962085ae4d286ecae97678395d6).

**Cyfrin:** Verified. `Util` contract has been deprecated.
