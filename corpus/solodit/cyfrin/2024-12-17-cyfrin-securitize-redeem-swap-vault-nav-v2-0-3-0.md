---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-3-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Incorrect/misleading comments
vuln_class: []
---

# Incorrect/misleading comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** Comments that do not accurately reflect the code's functionality can lead to misinterpretation during development, code review, and future maintenance.

```solidity
ISecuritizeNavProvider.sol
20: /**
21:  * @title ISecuritizeNavProvider
22:  * @dev Defines a common interface to get NAV (Native Asset Value) Rate to  //@audit-issue INFO incomplete comment
23:  */
```

In the instance below, it is also recommended to write the amount conversion formula.
```solidity
ISecuritizeNavProvider.sol
38:
39:     /**
40:      * @dev Set rate. It is expressed with the same decimal numbers as stable coin//@audit-issue INFO it is called liquidity token in other places, not "stable coin"
41:      */
42:     function setRate(uint256 _rate) external;//@audit-info same decimal to liquidity token
43:
44:     /**
45:      * @dev The asset:liquidity rate.//@audit-info INFO liquidityAmount = assetAmount * rate() / assetDecimals
46:      * @return The asset:liquidity rate.
47:      */
48:     function rate() external view returns (uint256);
49: }
```

```solidity
SecuritizeRedemption.sol
64: /**
65:     * @dev Throws if called by any account other than the owner.//@audit-issue INFO incorrect comment
66:     */
67:     modifier navProviderNonZero(address _address) {
68:         require(_address != address(0) , "NAV rate provider address can not be zero");
69:         _;
70:     }
```

```solidity
SecuritizeRedemption.sol
72:     /**
73:     * @dev Throws if called by any account other than the owner.//@audit-issue INFO incorrect comment
74:     */
75:     function initialize(address _asset, address _navProvider) public onlyProxy initializer navProviderNonZero(_navProvider) {
76:         __BaseDSContract_init();
77:         asset = IERC20(_asset);
78:         navProvider = ISecuritizeNavProvider(_navProvider);
79:     }
```
```solidity
ISecuritizeRedemption.sol
60:     /**
61:      * @dev The NAV rate provider implementation.//@audit-issue INFO misleading comment, it's not necessarily an implementation.
62:      * @return The address of the NAV rate provider.
63:      */
64:     function navProvider() external view returns (ISecuritizeNavProvider);
65:
66:     /**
67:      * @dev Update the NAV rate provider implementation.//@audit-issue INFO misleading comment, it's not necessarily an implementation.
68:      * @param _navProvider The NAV rate provider implementation address//@audit-issue INFO misleading comment, it's not necessarily an implementation.
69:      */
70:     function updateNavProvider(address _navProvider) external;
```

```solidity
ISecuritizeRedemption.sol
42:     /**
43:      * @dev The liquidity provider implementation.//@audit-issue INFO misleading comment, it's not necessarily an implementation.
44:      * @return The address of the liquidity provider.
45:      */
46:     function liquidityProvider() external view returns (ILiquidityProvider);
47:
48:     /**
49:      * @dev Update the liquidity provider implementation.//@audit-issue INFO misleading comment, it's not necessarily an implementation.
50:      * @param _liquidityProvider The liquidity provider implementation address//@audit-issue INFO misleading comment, it's not necessarily an implementation.
51:      */
52:     function updateLiquidityProvider(address _liquidityProvider) external;
```

```solidity
CollateralLiquidityProvider.sol
56:     /**
57:      * @dev Throws if called by any account other than the owner.//@audit-issue INFO misleading comment, it's not the owner
58:      */
59:     modifier onlySecuritizeRedemption() {
60:         if (address(securitizeRedemption) != _msgSender()) {
61:             revert RedemptionUnauthorizedAccount(_msgSender());
62:         }
63:         _;
64:     }
```

```solidity
AllowanceLiquidityProvider.sol
55:     /**
56:      * @dev Throws if called by any account other than the owner.//@audit-issue INFO wrong comment
57:      */
58:     modifier onlySecuritizeRedemption() {
59:         if (address(securitizeRedemption) != _msgSender()) {
60:             revert RedemptionUnauthorizedAccount(_msgSender());
61:         }
62:         _;
63:     }
```

**Securitize:** Fixed in commit [8254e8](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/8254e84a8bd2579780cc7b3b1ffa4b9821bcd505).

**Cyfrin:** Verified.
