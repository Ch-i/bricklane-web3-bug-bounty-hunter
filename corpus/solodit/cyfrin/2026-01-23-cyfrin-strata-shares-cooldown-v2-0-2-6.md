---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Coverage depends on raw sharesCooldown balances and can be griefed
vuln_class: []
---

# Coverage depends on raw sharesCooldown balances and can be griefed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** `coverage()` is derived from `totalAssetsUnlocked()`, which subtracts convertToAssets(vault.balanceOf(address(sharesCooldown)))` from tranche NAVs.

```solidity
    function totalAssetsUnlocked() public view returns (uint256 jrtNav, uint256 srtNav) {
        (jrtNav, srtNav, ) = accounting.totalAssetsT0();

        uint256 jrtNavLocked = jrtVault.convertToAssets(jrtVault.balanceOf(address(sharesCooldown)));
        uint256 srtNavLocked = srtVault.convertToAssets(srtVault.balanceOf(address(sharesCooldown)));

        jrtNav = jrtNav > jrtNavLocked ? jrtNav - jrtNavLocked : 0;
        srtNav = srtNav > srtNavLocked ? srtNav - srtNavLocked : 0;
        return (jrtNav, srtNav);
    }
```

This means coverage depends on the raw ERC20 share balances held by SharesCooldown, not on its internal `activeRequests`. As a result, shares sent directly to `SharesCooldown` become permanently “locked” from the accounting perspective and will distort coverage forever.

**Recommended Mitigation:** Prevent direct transfer of shares to SharesCooldown so that excess balance cannot affect coverage.

**Strata:** **Cyfrin:**
