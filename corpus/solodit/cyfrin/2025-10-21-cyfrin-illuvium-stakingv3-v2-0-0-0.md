---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Calling `StakingVault::notifyRewardAmount` on empty vault leaves ILV stuck
vuln_class: []
---

# Calling `StakingVault::notifyRewardAmount` on empty vault leaves ILV stuck

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** `StakingVault::notifyRewardAmount` is the vault’s reward hook that updates the rewards-per-share accumulator (`accIlvPerShare`) so stakers can later claim ILV. It is called by [`L2RevenueDistributorV3::_applyAllocation`](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/src/L2RevenueDistributorV3.sol#L500-L504) after it has already transferred ILV to the vault:
```solidity
if (pool.kind == PoolKind.Vault) {
    // Transfer ILV to the vault and notify
    ilv.safeTransfer(pool.recipient, amount);
    IStakingVaultMinimal(pool.recipient).notifyRewardAmount(amount);
} else {
```

If `notifyRewardAmount` is invoked while `totalStaked == 0`, [`StakingVault::notifyRewardAmount`](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/src/StakingVault.sol#L330-L338) returns early and the transferred ILV is not added to `accIlvPerShare`:
```solidity
function notifyRewardAmount(uint256 ilvAmount)
    external
    override
    nonReentrant
    whenNotPaused
    onlyRole(DISTRIBUTOR_ROLE)
{
    // If no rewards are provided, return
    if (ilvAmount == 0) return;
```

As a result, those tokens sit in the vault and are not claimable via normal flows; there is no built-in sweep/buffer to recover them later.

**Impact:** The funds are effectively stuck: neither users nor admins can redistribute or withdraw the stranded ILV using existing code paths. In practice, the only recovery is to upgrade the contract. Until then, the ILV remains idle in the vault.

**Recommended Mitigation:** * Vault-side buffer: Track `unallocatedRewards` and always add incoming amounts to it; when `totalStaked > 0`, fold the entire buffer into `accIlvPerShare`.
* Distributor-side skip/carry: Before transferring to a vault, check `totalStaked() > 0`. If zero, skip the transfer and record a per-pool carry to retry later (or divert to a claimable bucket).
* Hard fail on empty vault: In `notifyRewardAmount`, revert when `totalStaked == 0` to prevent accidental stranding (e.g., `require(totalStaked > 0, "No stakers")`). Together with per-pool try/catch or skip logic in the distributor to avoid whole-tx failures.

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified; Vault-side buffer mitigation was implemented.
