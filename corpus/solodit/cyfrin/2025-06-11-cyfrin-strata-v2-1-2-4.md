---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: '`MetaVault::redeem` erroneously calls `ERC4626Upgradeable::withdraw` when
  attempting to redeem `USDe` from `pUSDeVault`'
vuln_class: []
---

# `MetaVault::redeem` erroneously calls `ERC4626Upgradeable::withdraw` when attempting to redeem `USDe` from `pUSDeVault`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Unlike `MetaVault::deposit`, `MetaVault::mint`, and `MetaVault::withdraw` which all invoke the corresponding `IERC4626` function, `MetaVault::redeem` erroneously calls `ERC4626Upgradeable::withdraw` when attempting to redeem `USDe` from `pUSDeVault`:

```solidity
function redeem(address token, uint256 shares, address receiver, address owner) public virtual returns (uint256) {
    if (token == asset()) {
        return withdraw(shares, receiver, owner);
    }
    ...
}
```

**Impact:** The behavior of `MetaVault::redeem` differs from that which is expected depending on whether `token` is specified as `USDe` or one of the other supported vault tokens.

**Recommended Mitigation:**
```diff
    function redeem(address token, uint256 shares, address receiver, address owner) public virtual returns (uint256) {
        if (token == asset()) {
--          return withdraw(shares, receiver, owner);
++          return redeem(shares, receiver, owner);
        }
        ...
    }
```

**Strata:** Fixed in commit [7665e7f](https://github.com/Strata-Money/contracts/commit/7665e7f3cd44d8a025f555737677d2014f4ac8a8).

**Cyfrin:** Verified.
