---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Consider enforcing minimum redemption amounts in `PublicStockOffRamp, SecuritizeOffRamp::redeem`
vuln_class: []
---

# Consider enforcing minimum redemption amounts in `PublicStockOffRamp, SecuritizeOffRamp::redeem`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The `PublicStockOnRamp` contract enforces a minimum subscription amount check via the `validateMinSubscriptionAmount` modifier to prevent dust trades:

```solidity
 modifier validateMinSubscriptionAmount(uint256 _amount) {
        if (_amount < minSubscriptionAmount) {
            revert MinSubscriptionAmountError();
        }
        _;
    }
```
However, the `PublicStockOffRamp::redeem`  and `SecuritizeOffRamp::redeem` lacks an equivalent validation on the `_assetAmount` input parameter. This allows users to submit redemption requests with arbitrarily small amounts (e.g., _assetAmount = 1).

**Impact:** * Dust redemptions that pass signature validation but fail at slippage check waste gas for the operator.
* possible problem due rounding issues in the amm


**Recommended Mitigation:** Add a minimum redemption amount validation to the offramp contracts, consistent with the OnRamp pattern:

**Securitize:** Acknowledged.
