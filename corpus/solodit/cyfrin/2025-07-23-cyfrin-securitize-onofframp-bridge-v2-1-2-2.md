---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: '`liquidityProviderWallet` is not set during initialization'
vuln_class: []
---

# `liquidityProviderWallet` is not set during initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** In `AllowanceLiquidityProvider::initialize`, one of the key properties, `liquidityProviderWallet`, is not initialized. This property is declared as a public variable but never set during contract initialization. Since the contract does not enforce or set this value at any point in `initialize`, any functionality that depends on `liquidityProviderWallet` may behave incorrectly.

```solidity
address public liquidityProviderWallet;
```

**Impact:** Until `liquidityProviderWallet` is set, functions like `_availableLiquidity()` and `supplyTo()` will rely on the default address(0) value. This could result in:

- Returning an incorrect liquidity value (typically zero).

- Causing failed or unexpected behavior during redemptions, since transferFrom(address(0), ...) will fail.

**Recommended Mitigation:** Update the `initialize` function to accept a `_liquidityProviderWallet` parameter and ensure it is validated and assigned:

```solidity
function initialize(
    address _liquidityToken,
    address _recipient,
    address _securitizeOffRamp,
    address _liquidityProviderWallet
) public onlyProxy initializer {
    if (_recipient == address(0)) revert NonZeroAddressError();
    if (_liquidityToken == address(0)) revert NonZeroAddressError();
    if (_securitizeOffRamp == address(0)) revert NonZeroAddressError();
    if (_liquidityProviderWallet == address(0)) revert NonZeroAddressError();

    __BaseContract_init();
    recipient = _recipient;
    liquidityToken = IERC20(_liquidityToken);
    securitizeOffRamp = ISecuritizeOffRamp(_securitizeOffRamp);
    liquidityProviderWallet = _liquidityProviderWallet;
}
```

This ensures that `liquidityProviderWallet` is set once during contract initialization and cannot be accidentally or maliciously left uninitialized.

**Securitize:** Fixed in commit [ab08ae](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/ab08aea2c8c67ca311dcf46cd747621f84a14505).

**Cyfrin:** Verified.
