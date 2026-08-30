---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Missing PausableUpgradable initialization in SecuritizeSwap contract initialization
vuln_class: []
---

# Missing PausableUpgradable initialization in SecuritizeSwap contract initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** The `SecuritizeSwap` contract inherits from `PausableUpgradeable` (through `BaseSecuritizeSwap`) but doesn't call `__Pausable_init()` during initialization. While this currently doesn't affect functionality since the default state (paused = false) matches the initialization state, it's a deviation from best practices.

**Recommended Mitigation:** For completeness and following best practices, add the Pausable initialization:
```solidity
function initialize(...) public override initializer onlyProxy {
    BaseSecuritizeSwap.initialize(
        _dsToken,
        _stableCoin,
        _erc20Token,
        _issuerWallet,
        _liquidityProvider,
        _externalCollateralRedemption,
        _collateralToken,
        _swapMode
    );
    __BaseDSContract_init();
    __Pausable_init();
}
```

**Securitize:** Fixed in commit [637bcc](https://bitbucket.org/securitize_dev/securitize-swap/commits/637bcce49acab125b54caeaa98fffc1790782b60).

**Cyfrin:** Verified.
