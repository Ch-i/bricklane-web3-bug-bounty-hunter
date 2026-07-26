---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-4-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Unnecessary arithmetic validation within `AngstromL2::withdrawProtocolRevenue`
  can be removed
vuln_class: []
---

# Unnecessary arithmetic validation within `AngstromL2::withdrawProtocolRevenue` can be removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `AngstromL2::withdrawProtocolRevenue` first validates whether `unclaimedProtocolRevenueInEther` is sufficient to cover a withdrawal of `amount` by the owner; however, this is not necessary and can be removed as the subsequent decrement would panic revert due to underflow:

```solidity
function withdrawProtocolRevenue(uint160 assetId, address to, uint256 amount) public {
    _checkOwner();

    if (assetId == NATIVE_CURRENCY_ID) {
@>      if (!(amount <= unclaimedProtocolRevenueInEther)) {
            revert AttemptingToWithdrawLPRewards();
        }
@>      unclaimedProtocolRevenueInEther -= amount.toUint128();
    }

    UNI_V4.transfer(to, assetId, amount);
}
```

**Recommended Mitigation:**
```diff
function withdrawProtocolRevenue(uint160 assetId, address to, uint256 amount) public {
    _checkOwner();

    if (assetId == NATIVE_CURRENCY_ID) {
-       if (!(amount <= unclaimedProtocolRevenueInEther)) {
-           revert AttemptingToWithdrawLPRewards();
-       }
        unclaimedProtocolRevenueInEther -= amount.toUint128();
    }

    UNI_V4.transfer(to, assetId, amount);
}
```

**Sorella Labs:** Fixed in commit [ffb9fb2](https://github.com/SorellaLabs/l2-angstrom/commit/ffb9fb20e5b0afbf6996ef9528ef10acd8c94f91#diff-0e68badc81333f3e60fad8069459c6e57e1ac84f433fb40f23cda776b9f9442b).

**Cyfrin:** Verified. The validation along with `unclaimedProtocolRevenueInEther` itself have been removed since revenue paid in the underlying currency is now distinct from rewards accounted by ERC-6909 balance.
