---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Upgradeable contracts missing _disableInitializers() in constructors
vuln_class: []
---

# Upgradeable contracts missing _disableInitializers() in constructors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The following contracts are upgradeable but do not call `_disableInitializers()` in their constructors:
- `MintingAssetProvider`
- `AllowanceAssetProvider`
- `SecuritizeOnRamp`
- `MbpsFeeManager`
- `SecuritizeOffRamp`
- `AllowanceLiquidityProvider`
- `CollateralLiquidityProvider`

In upgradeable contract patterns (such as those using OpenZeppelin's UUPS or Transparent proxies), the implementation (logic) contract is deployed independently from the proxy. If the implementation contract does not call `_disableInitializers()` in its constructor, it can be initialized directly by anyone, which is not intended and can lead to security risks. ([reference](https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable#initializing_the_implementation_contract))

**Impact:** If the implementation contract is initialized directly, an attacker could set themselves as the owner or assign other privileged roles, potentially interfering with the upgrade process or causing confusion. While this does not directly affect the proxy's state, it can break upgradeability, allow denial of service, or create unexpected behaviors in the system.

**Recommended Mitigation:** Add a constructor to each affected contract that calls `_disableInitializers()`. This ensures the implementation contract cannot be initialized or reinitialized, preventing any unauthorized or accidental initialization outside the proxy context.

```solidity
constructor() {
    _disableInitializers();
}
```

Add this to each of the affected contracts.

**Securitize:** Fixed in commit [088048](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/0880486f4e75df252c5e6a773b2f09a4956fdb87).

**Cyfrin:** Verified.
