---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Missing minimum deposit enforcement
vuln_class: []
---

# Missing minimum deposit enforcement

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `Licredity::depositFungible` function does not enforce a minimum deposit size. This allows users to create or add to positions with extremely small, economically insignificant amounts of collateral (i.e., "dust").

**Impact:** Allowing dust deposits can lead to state bloat. A malicious actor could create a large number of positions with negligible value, cluttering the contract's storage. What is more, not having such check increases the overall attack vector surface in the contract.

**Recommended Mitigation:** Introduce a minimum deposit amount check within the `depositFungible` function. This can be a hardcoded constant or a configurable variable. If the deposit amount is below this threshold, the transaction should revert.

```diff
// ...existing code...
+    uint256 private constant MIN_DEPOSIT_AMOUNT = 10000; // Example value, should be set appropriately

	 function depositFungible(uint256 positionId) external payable {
        Position storage position = positions[positionId];
        (Fungible fungible, uint256 amount) = _getStagedFungibleAndAmount();

+        require(amount >= MIN_DEPOSIT_AMOUNT, "Deposit amount too small");
		...
    }
// ...existing code...
```

**Licredity:** Acknowledged. But we don't plan to fix this as 1) unclear it will cause any problem; 2) there are other ways to create dust assets / dust positions; and 3) prefer to not have magic numbers and suggested mitigation isn't practical - 0.001 BTC is meaningfully different from 0.001 PEPE.
