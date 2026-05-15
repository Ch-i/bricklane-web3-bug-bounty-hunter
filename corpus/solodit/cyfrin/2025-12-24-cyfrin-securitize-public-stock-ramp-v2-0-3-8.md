---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Cache decimals of underlying asset at initialization in `SecuritizeAmmNavProvider`
vuln_class: []
---

# Cache decimals of underlying asset at initialization in `SecuritizeAmmNavProvider`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeAmmNavProvider` has no function to change the value of `asset` after initialization. Since ERC20 tokens typically never changed their decimals, the asset decimals can be cached at initialization to save external calls in `quoteBuyBase, quoteSellBase, executeBuyBase, executeSellBase`.

Since the decimals are only used to calculate `scaleDown`, can just cache this eg:

```diff
contract SecuritizeAmmNavProvider {
    /* snip : existing storage layout */
+   uint256 public SCALE_DOWN;

    function initialize(uint256 _baseReserves, uint256 _quoteReserves, address _asset) public onlyProxy initializer {
        /* snip : existing code */
        asset = IERC20Metadata(_asset);
+       uint8 d = asset.decimals();
+       require(d <= 18, "decimals > 18");
+       SCALE_DOWN = 10 ** (18 - d);
    }
```

Then the following code can be removed from `quoteBuyBase, quoteSellBase, executeBuyBase, executeSellBase`:
```diff
-       uint8 d = asset.decimals();
-       require(d <= 18, "decimals > 18");
-       uint256 scaleDown = 10 ** (18 - d);
```

And just use `SCALE_DOWN` where it is required; this is more efficient and also reduces duplicated code, increasing code quality.

If there is a need to change the asset or the `SCALE_DOWN` factor, just add a new privileged function which sets a new `asset` and recalculates `SCALE_DOWN` using the new asset's decimals.

**Securitize:** Acknowledged.
