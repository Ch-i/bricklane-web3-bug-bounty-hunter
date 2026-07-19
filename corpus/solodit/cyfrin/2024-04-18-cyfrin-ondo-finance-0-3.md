---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: '`InstantMintTimeBasedRateLimiter::_setInstantMintLimit` and `_setInstantRedemptionLimit`
  can make subsequent calls to `_checkAndUpdateInstantMintLimit` and `_checkAndUpdateInstantRedemptionLimit`
  revert due to underflow'
vuln_class: []
---

# `InstantMintTimeBasedRateLimiter::_setInstantMintLimit` and `_setInstantRedemptionLimit` can make subsequent calls to `_checkAndUpdateInstantMintLimit` and `_checkAndUpdateInstantRedemptionLimit` revert due to underflow

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `InstantMintTimeBasedRateLimiter::_checkAndUpdateInstantMintLimit` [L103-106](https://github.com/ondoprotocol/rwa-internal/blob/6747ebada1c867a668a8da917aaaa7a0639a5b7a/contracts/InstantMintTimeBasedRateLimiter.sol#L103-L106) subtracts the currently minted amount from the mint limit:
```solidity
require(
  amount <= instantMintLimit - currentInstantMintAmount,
  "RateLimit: Mint exceeds rate limit"
);
```

If `_setInstantMintLimit` is used to set `instantMintLimit < currentInstantMintAmount`, subsequent calls to this function will revert due the underflow. The same is true for `_setInstantRedemptionLimit` and `_checkAndUpdateInstantRedemptionLimit`.

**Impact:** `InstantMintTimeBasedRateLimiter::_setInstantMintLimit` and `_setInstantRedemptionLimit` can make subsequent calls to `_checkAndUpdateInstantMintLimit` and `_checkAndUpdateInstantRedemptionLimit` revert due to underflow.

**Recommended Mitigation:** Explicitly handle the case where the limit is smaller than the current mint/redemption amount:
```solidity
function _checkAndUpdateInstantMintLimit(uint256 amount) internal {
    require(
      instantMintLimit > currentInstantMintAmount && amount <= instantMintLimit - currentInstantMintAmount,
      "RateLimit: Mint exceeds rate limit"
    );
}

function _checkAndUpdateInstantRedemptionLimit(uint256 amount) internal {
    require(
      instantRedemptionLimit > currentInstantRedemptionAmount && amount <= instantRedemptionLimit - currentInstantRedemptionAmount,
      "RateLimit: Redemption exceeds rate limit"
    );
}
```

**Ondo:**
Fixed in commit [fb8ecff](https://github.com/ondoprotocol/rwa-internal/commit/fb8ecff80960c8c891ddc206c6f6f27a620e42d6).

**Cyfrin:** Verified.
