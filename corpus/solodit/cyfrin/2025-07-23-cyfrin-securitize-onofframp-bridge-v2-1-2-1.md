---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Missing validation check for liquidityToken
vuln_class: []
---

# Missing validation check for liquidityToken

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `CollateralLiquidityProvider::initialize()` function does **not verify** that the `liquidityToken` of the passed `securitizeOffRamp`'s `liquidityProvider()` matches the expected token. This check is present in `setExternalCollateralRedemption()` but missing here.

**Impact:** A mismatched `liquidityToken` could lead to misconfiguration, loss of funds, or unintended asset interactions.

 **Recommended Mitigation:**
Add a check in the `initialize()` function to verify that the `liquidityToken` of the `securitizeOffRamp`’s liquidity provider matches the `_liquidityToken` parameter:

```solidity
function initialize(
    address _liquidityToken,
    address _recipient,
    address _securitizeOffRamp
) public onlyProxy initializer {
    if (_recipient == address(0) || _liquidityToken == address(0) || _securitizeOffRamp == address(0)) {
        revert NonZeroAddressError();
    }

    address expectedToken = ILiquidityProvider(
        ISecuritizeOffRamp(_securitizeOffRamp).liquidityProvider()
    ).liquidityToken();

    if (expectedToken != _liquidityToken) {
        revert LiquidityTokenMismatch();
    }

    __BaseContract_init();
    recipient = _recipient;
    liquidityToken = IERC20(_liquidityToken);
    securitizeOffRamp = ISecuritizeOffRamp(_securitizeOffRamp);
}
```

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.
