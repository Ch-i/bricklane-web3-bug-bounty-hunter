---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Equal distribution fallback logic error
vuln_class: []
---

# Equal distribution fallback logic error

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** In the `L2RevenueDistributorV3::_allocateEqual()` function, when the total reserve units are zero, the contract falls back to equal distribution of remaining ILV to active reserve-weighted pools. However, the eligibility check for Vault pools includes the condition `units[i] > 0`, but `units[i]` is always zero in this scenario (since `totalUnits` is zero). This results in Vault pools being incorrectly excluded from the equal distribution, allowing only Claimable pools to receive funds.

**Impact:** Vault pools may not receive their intended share of ILV distributions when reserve calculations result in zero units, leading to unfair allocation of rewards. This could cause loss of expected yield for users staking in Vault pools, potentially undermining the protocol's incentive mechanisms.

**Recommended Mitigation:** Modify the eligibility check in `_allocateEqual()` to not depend on `units[i]` for Vault pools when in equal distribution mode. Instead, simply check that the pool is active and reserve-weighted. For example:

```solidity
bool isEligible = (pool.kind == PoolKind.Claimable) || (pool.kind == PoolKind.Vault);
```

This ensures both Claimable and Vault pools are included in the equal distribution when reserves are zero. Additionally, consider adding a comment to clarify this behavior.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.

\clearpage
