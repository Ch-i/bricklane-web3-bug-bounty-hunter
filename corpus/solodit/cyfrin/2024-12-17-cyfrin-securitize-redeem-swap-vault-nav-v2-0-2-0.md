---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Missing input validation in privileged functions
vuln_class: []
---

# Missing input validation in privileged functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** Admin functions lack proper parameter validation, which could lead to unintended state changes if incorrect values are provided. While admin users are expected to act correctly, human error remains possible.

```solidity
SecuritizeRedemption.sol
75:     function initialize(address _asset, address _navProvider) public onlyProxy initializer navProviderNonZero(_navProvider) {
76:         __BaseDSContract_init();
77:         asset = IERC20(_asset);//@audit-issue INFO non zero check
78:         navProvider = ISecuritizeNavProvider(_navProvider);
79:     }
80:

SecuritizeRedemption.sol
81:     function updateLiquidityProvider(address _liquidityProvider) onlyOwner external {
82:         address oldProvider = address(liquidityProvider);
83:         liquidityProvider = ILiquidityProvider(_liquidityProvider);//@audit-issue INFO non zero check
84:         emit LiquidityProviderUpdated(oldProvider, address(liquidityProvider));
85:     }

SecuritizeRedemption.sol
87:     function updateNavProvider(address _navProvider) onlyOwner navProviderNonZero(_navProvider) external {
88:         address oldProvider = address(navProvider);
89:         navProvider = ISecuritizeNavProvider(_navProvider);//@audit-issue INFO non zero check
90:         emit NavProviderUpdated(oldProvider, address(navProvider));
91:     }
```

```solidity
CollateralLiquidityProvider.sol
66:     function initialize(address _recipient, address _liquidityToken, address _securitizeRedemption) public onlyProxy initializer {
67:         __BaseDSContract_init();
68:         recipient = _recipient;//@audit-issue LOW sanity check
69:         liquidityToken = IERC20(_liquidityToken);
70:         securitizeRedemption = ISecuritizeRedemption(_securitizeRedemption);
71:     }

98:
99:     function setCollateralProvider(address _collateralProvider) external onlyOwner {
100:         address oldAddress = address(collateralProvider);
101:         collateralProvider = _collateralProvider;//@audit-issue LOW sanity check
102:         emit CollateralProviderUpdated(oldAddress, address(collateralProvider));
103:     }
```

```solidity
AllowanceLiquidityProvider.sol
65:     function initialize(address _recipient, address _liquidityToken, address _securitizeRedemption) public onlyProxy initializer {
66:         __BaseDSContract_init();
67:         recipient = _recipient;//@audit-issue LOW sanity check
68:         liquidityToken = IERC20(_liquidityToken);
69:         securitizeRedemption = ISecuritizeRedemption(_securitizeRedemption);
70:     }

85:     function setAllowanceProviderWallet(address _liquidityProviderWallet) external onlyOwner {
86:         address oldAddress = liquidityProviderWallet;
87:         liquidityProviderWallet = _liquidityProviderWallet;//@audit-issue sanity check
88:         emit AllowanceLiquidityProviderWalletUpdated(oldAddress, liquidityProviderWallet);
89:     }
```

**Securitize:** Fixed in commit [8254e8](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/8254e84a8bd2579780cc7b3b1ffa4b9821bcd505).

**Cyfrin:** Verified.
