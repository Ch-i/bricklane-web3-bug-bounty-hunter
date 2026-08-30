---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: '`PreDepositVault::initialize` should not be exposed as public'
vuln_class: []
---

# `PreDepositVault::initialize` should not be exposed as public

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** `PreDepositVault::initialize` is currently exposed as public. Based on the `pUSDeVault` and `yUSDeVault` implementations that invoke this super function, it is not intended. While this does not appear to be exploitable or cause any issues that prevent initialization, it would be better to mark this base implementation as internal and use the `onlyInitializing` modifier instead.

```diff
    function initialize(
        address owner_
        , string memory name
        , string memory symbol
        , IERC20 USDe_
        , IERC4626 sUSDe_
        , IERC20 stakedAsset
--  ) public virtual initializer {
++  ) internal virtual onlyInitializing {
        __ERC20_init(name, symbol);
        __ERC4626_init(stakedAsset);
        __Ownable_init(owner_);

        USDe = USDe_;
        sUSDe = sUSDe_;
    }
```

**Strata:** Fixed in commits [6ac05c2](https://github.com/Strata-Money/contracts/commit/6ac05c232a47de6e9935fd6e20af1f0c4540c457) and [def7d36](https://github.com/Strata-Money/contracts/commit/def7d360225f49662c73bf968d63d935c82d9d0e).

**Cyfrin:** Verified. `PreDepositVault::initialize` is now marked as internal and uses the `onlyInitializing` modifier.
