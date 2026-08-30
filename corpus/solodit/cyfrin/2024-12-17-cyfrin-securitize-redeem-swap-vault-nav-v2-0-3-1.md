---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Naming improvements
vuln_class: []
---

# Naming improvements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** While functionally correct, certain function/modifier names could be more descriptive to better reflect their purpose and implementation.

```solidity
SecuritizeRedemption.sol
64:     /**
65:     * @dev Throws if called by any account other than the owner.
66:     */
67:     modifier navProviderNonZero(address _address) {//@audit-issue INFO better naming addressNonZero
68:         require(_address != address(0) , "NAV rate provider address can not be zero");
69:         _;
70:     }
```

**Securitize:** Fixed in commit [8254e8](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/8254e84a8bd2579780cc7b3b1ffa4b9821bcd505).

**Cyfrin:** Verified.
