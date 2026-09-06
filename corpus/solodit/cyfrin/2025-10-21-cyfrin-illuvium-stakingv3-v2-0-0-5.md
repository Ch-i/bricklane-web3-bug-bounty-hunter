---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Dust rewards can become permanently locked
vuln_class: []
---

# Dust rewards can become permanently locked

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description**
During `distribute()`, leftover amounts (“dust”) can remain as a remainder. These remainders are attempted to be allocated to the first eligible participant. However, if the remainder is **smaller than `totalStaked / 1e18`**, the reward is not distributed and instead gets permanently stuck in the contract.

```solidity
if (rwDistributed < remainder) {
    uint256 dust = remainder - rwDistributed;
    rwDistributed += _allocateFirstEligible(dust, poolCount, units);
}
```

**Impact**
Over time, repeated distributions with such small remainders accumulate, leading to a growing amount of ILV locked in the contract and never reaching stakers.

**Recommended Mitigation**
Apply the threshold check **inside `_applyAllocation`** to ensure that only meaningful amounts are distributed.

```solidity
function _applyAllocation(Pool storage pool, uint256 amount) internal {
    // skip if dust is too small to be distributed
    if (amount * Constants.ACC_PRECISION <= pool.totalStaked) {
        return;
    }

    if (pool.kind == PoolKind.Vault) {
        ilv.safeTransfer(pool.recipient, amount);
        IStakingVaultMinimal(pool.recipient).notifyRewardAmount(amount);
    } else {
        pool.pendingIlv += amount;
    }
}
```

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
