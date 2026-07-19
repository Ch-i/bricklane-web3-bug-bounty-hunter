---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Consider adding a minimum deposit amount in `StakingVault`
vuln_class: []
---

# Consider adding a minimum deposit amount in `StakingVault`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** [`StakingVault.deposit`](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/src/StakingVault.sol#L140-L141) accepts any positive `amount`, including 1 wei. Extremely small stakes don’t make economic sense and can amplify integer-rounding edge cases in the rewards-per-share model. These style of deposits are only used by black hats to manipulate vaults.

Consider adding a configurable minimum deposit threshold and enforce it in `deposit`:

```solidity
error DepositAmountTooSmall(uint256 amount, uint256 minDeposit);

uint256 public minDeposit; // set by admin (e.g., during initialize), adjustable via setter + event

function setMinDeposit(uint256 newMin) external onlyRole(ADMIN_ROLE) {
    minDeposit = newMin;
    emit MinDepositUpdated(newMin);
}

function deposit(uint256 amount, uint64 lockStakeDuration) external whenNotPaused nonReentrant returns (uint256) {
    if (amount < minDeposit) revert DepositAmountTooSmall(amount, minDeposit);
    // ...existing logic...
}
```
**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
