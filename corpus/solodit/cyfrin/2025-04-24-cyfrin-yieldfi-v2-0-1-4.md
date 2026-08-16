---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Direct YToken deposits can lock funds below minimum withdrawal threshold
vuln_class: []
---

# Direct YToken deposits can lock funds below minimum withdrawal threshold

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In [`Manager::deposit`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L134-L155), there is a check enforcing a minimum deposit amount inside [`Manager::_validate`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L125-L126):

```solidity
uint256 normalizedAmount = _normalizeAmount(_yToken, _asset, _amount);
require(IERC4626(_yToken).convertToShares(normalizedAmount) >= minSharesInYToken[_yToken], "!minShares");
```

A similar check exists in the [redeem flow](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L157-L197), again via [`Manager::_validate`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L130):

```solidity
require(_amount >= minSharesInYToken[_yToken], "!minShares");
```

However, no such minimum is enforced when depositing directly into a `YToken`. In both [`YToken::_deposit`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YToken.sol#L140) and [`YTokenL2::_deposit`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YTokenL2.sol#L150), the only requirement is:

```solidity
require(receiver != address(0) && assets > 0 && shares > 0, "!valid");
```

As a result, a user could deposit an amount that results in fewer shares than `minSharesInYToken[_yToken]`, which cannot be withdrawn through the `Manager` due to its minimum withdrawal check, effectively locking their funds.

**Impact:** Users can bypass the minimum share threshold by depositing directly into a `YToken`. If the resulting share amount is below the minimum allowed for withdrawal via the `Manager`, the user will be unable to exit their position. This can lead to unintentionally locked funds and a poor user experience.

**Recommended Mitigation:** Consider enforcing the `minSharesInYToken[_yToken]` threshold in `YToken::_deposit` and `YTokenL2::_deposit` to prevent deposits that are too small to be withdrawn. Additionally, consider validating post-withdrawal balances to ensure users are not left with non-withdrawable "dust" (i.e., require remaining shares to be either `0` or `> minSharesInYToken[_yToken]`).

**YieldFi:** Fixed in commit [`221c7d0`](https://github.com/YieldFiLabs/contracts/commit/221c7d0644af8fcb4d229d3e95e45323dc6f99a6)

**Cyfrin:** Verified. Minimum shares is now verified in the YToken contracts. Manager also verifies that there is no dust left after redeem.

\clearpage
