---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Unreachable code inside `sUSDeStrategy::reduceReserve`
vuln_class: []
---

# Unreachable code inside `sUSDeStrategy::reduceReserve`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The last line inside `sUSDeStrategy::reduceReserve`: `revert UnsupportedToken(token);` is unreachable.

`sUSDeStrategy::reduceReserve` can be called only via `StrataCDO::reduceReserve`, which before calling `strategy.reduceReserve(token, tokenAmount, treasury);` will call `uint256 baseAssets = strategy.convertToAssets(token, tokenAmount, Math.Rounding.Floor);`.

`sUSDeStrategy::convertToAssets` already reverts for unsupported tokens:

```
    function convertToAssets (address token, uint256 tokenAmount, Math.Rounding rounding) external view returns (uint256) {
        if (token == address(sUSDe)) { // if sUSDe, use previewRedeem or previewMint
            return rounding == Math.Rounding.Floor
                ? sUSDe.previewRedeem(tokenAmount) // aka convertToAssets(tokenAmount)
                : sUSDe.previewMint(tokenAmount); // aka convertToAssetsCeil(tokenAmount)
        }
        if (token == address(USDe)) { // if USDe, return the input amount
            return tokenAmount;
        }
        revert UnsupportedToken(token);
    }
```

**Strata:**
Acknowledged; we prefer to leave the current behaviour. You are absolutely right that this revert is unreachable under the current conditions, but to keep it consistent with the other methods, the Strategy must check every operation on tokens to see if it is supported.

**Cyfrin:** Acknowledged.
