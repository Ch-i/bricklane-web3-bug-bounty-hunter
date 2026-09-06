---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Unused parameter in address validation modifier SecuritizeOffRamp::addressNonZero
vuln_class: []
---

# Unused parameter in address validation modifier SecuritizeOffRamp::addressNonZero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `addressNonZero` modifier used in `SecuritizeOffRamp::initialize()`, `SecuritizeOffRamp::updateLiquidityProvider()`, and `SecuritizeOffRamp::updateNavProvider()` functions accepts a `string memory parameter` argument but never uses it within the modifier logic.
This parameter appears to be intended for providing context about which address parameter is being validated, but it remains unused in the error handling.

```solidity
modifier addressNonZero(address _address, string memory parameter) {
    if (_address == address(0)) {
        revert NonZeroAddressError();
    }
    _;
}
```

The modifier is called with descriptive strings like "asset", "navProvider", "feeManager", and "liquidityProvider" but this contextual information is not utilized in the error reporting or validation logic. For comparison, other contracts in the codebase use similar address validation modifiers without unused parameters, such as `addressNotZero` in `USDCBridge.sol` which correctly implements the validation without taking unnecessary parameters.

**Impact:** The unused parameter creates inconsistent code patterns and represents a missed opportunity to provide meaningful error context when address validation fails.

**Recommended Mitigation:** Remove the unused parameter from the `addressNonZero` modifier to maintain consistency with similar validation patterns in other contracts:

```diff
- modifier addressNonZero(address _address, string memory parameter) {
+ modifier addressNonZero(address _address) {
    if (_address == address(0)) {
        revert NonZeroAddressError();
    }
    _;
}
```

And update all usage sites to remove the string parameter:

```diff
- addressNonZero(_asset, "asset")
+ addressNonZero(_asset)
- addressNonZero(_navProvider, "navProvider")
+ addressNonZero(_navProvider)
- addressNonZero(_feeManager, "feeManager")
+ addressNonZero(_feeManager)
- addressNonZero(_liquidityProvider, "liquidityProvider")
+ addressNonZero(_liquidityProvider)
```

**Securitize:** Fixed in commit [fd5511](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/fd5511077e368ee1d84f2695fe67b77bb185d6a3).

**Cyfrin:** Verified.
