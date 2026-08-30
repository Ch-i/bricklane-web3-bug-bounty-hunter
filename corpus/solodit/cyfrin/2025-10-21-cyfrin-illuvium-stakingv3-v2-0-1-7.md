---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-1-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Inconsistent `recipient` handling for claimable pools
vuln_class: []
---

# Inconsistent `recipient` handling for claimable pools

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** [`L2RevenueDistributorV3.Pool.recipient`](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/src/L2RevenueDistributorV3.sol#L73) is documented as “vault address or claimable recipient key”:
```solidity
address recipient; // vault address or claimable recipient key
```

However, `L2RevenueDistributorV3::claimPool(id, to)` ignores it and transfers ILV to the caller-supplied `to`. Meanwhile, the [deploy script](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/script/Deployer.s.sol#L219) sets a dummy `pool.recipient = address(0x1111)` for the claimable pool, while allowlisting `helperConfig.getL1PoolAdmin()` elsewhere. This mismatch is confusing and brittle if future logic starts using `recipient`.

Consider either clarifying the documentation that `recipient` is not used for claimable pools or change `claimPool` to send to `recipient` and remove the placeholder in the deploy script.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified; The documentation regarding recipient was made more clear.

\clearpage
