---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_Redemption_Core::iClaimYield` reverts on empty pool (`totalSupply ==
  0`)'
vuln_class: []
---

# `STBL_Redemption_Core::iClaimYield` reverts on empty pool (`totalSupply == 0`)

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_Redemption::claimYield` routes to `STBL_Redemption_Core::iClaimYield`:

```solidity
function iClaimYield() internal {
    AssetDefinition memory AssetData = registry.fetchAssetData(AssetID);
    uint256 _value = iSTBL_YieldDistributor(AssetData.rewardDistributor).claim(NFTID);
    rewardIndex += (_value * MULTIPLIER) / totalSupply;
}
```

When `totalSupply == 0` (fresh pool, or after full LP exit), the division panics with Solidity `0x12` (division by zero). This contradicts the public expectation that anyone can safely call `claimYield` as upkeep.

**Impact:** Unexpected Revert / DoS

**Recommended Mitigation:** Guard the empty-pool state before division:

```solidity
function iClaimYield() internal {
    if (totalSupply == 0) return;
    AssetDefinition memory AssetData = registry.fetchAssetData(AssetID);
    uint256 _value = iSTBL_YieldDistributor(AssetData.rewardDistributor).claim(NFTID);
    rewardIndex += (_value * MULTIPLIER) / totalSupply;
}
```

**STBL:** Fixed in commit [68920b7](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-redemptions/commit/68920b7c46ea03a45dadc3d5e85e0aa602b4e28c).

**Cyfrin:** Verified. `iClaimYield` now reverts `STBL_Redemption_VaultInactive` when `totalSupply == 0`, replacing the division-by-zero panic with an explicit guard. Internal callers are unaffected since they only reach it while `totalSupply > 0`.
