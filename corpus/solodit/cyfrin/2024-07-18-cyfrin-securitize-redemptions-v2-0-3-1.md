---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: The `SecuritizeRedemption.updateLiquidityProvider` function emits the wrong
  information.
vuln_class: []
---

# The `SecuritizeRedemption.updateLiquidityProvider` function emits the wrong information.

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The `SecuritizeRedemption.updateLiquidityProvider` function emits the information that `oldProvider` is updated to `liquidityProvider`.
But the function allocates `_liquidityProvider` to `oldProvider` instead of `liquidityProvider`

In the `updateLiquidityProvider` function, it allocates new variable `_liquidityProvider` to `oldProvider` instead of `liquidityProvider` from L66.

```solidity
File: securitize_dev-bc-redemption-sc-32e23d5318be\contracts\redemption\SecuritizeRedemption.sol
65:     function updateLiquidityProvider(address _liquidityProvider) onlyOwner external override {
66:         address oldProvider = address(_liquidityProvider);
67:         liquidityProvider = ILiquidityProvider(_liquidityProvider);
68:         emit LiquidityProviderUpdated(oldProvider, address(liquidityProvider));
69:     }
```

From L67, `liquidityProvider` is also same as `_liquidityProvider`.
From L68, it emits same variables and this is wrong.


**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4)

**Cyfrin:** Verified.
