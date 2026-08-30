---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-4-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Inconsistent use of `override` keyword
vuln_class: []
---

# Inconsistent use of `override` keyword

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** We found that `override` keyword is being used inconsistently in several places.
It is recommended to use the `override` keyword consistently and reasonably.

```solidity
CollateralLiquidityProvider.sol
75:     function setExternalCollateralRedemption(address _externalCollateralRedemption) external override { //@audit override keyword
76:         externalCollateralRedemption = IRedemption(_externalCollateralRedemption);
77:     }
78:
79:     function setCollateralProvider(address _collateralProvider) external { //@audit no override keyword
80:         collateralProvider = _collateralProvider;
81:     }
```

**Securitize:** Fixed in commit [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28) and [334f49](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/334f4996bc79d0489122210ed54c5596bdcf4eb7).

**Cyfrin:** Verified.
