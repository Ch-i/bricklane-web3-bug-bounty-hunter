---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Use of modifier `nonZeroNavRate` in `SecuritizeOnRamp` and `SecuritizeOffRamp`
  results in duplicate external call with identical result
vuln_class: []
---

# Use of modifier `nonZeroNavRate` in `SecuritizeOnRamp` and `SecuritizeOffRamp` results in duplicate external call with identical result

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeOnRamp` and `SecuritizeOffRamp` both have modifier `nonZeroNavRate` which makes an external call to enforce a positive rate:
```solidity
modifier nonZeroNavRate() {
    if (navProvider.rate() <= 0) {
        revert NonZeroNavRateError();
    }
    _;
}
```

The problem is that the functions which use this modifier (such as `swap`) subsequently call a child function (such as `calculateDsTokenAmount`) which ends up making the same `navProvider.rate` external call again.

**Impact:** The same external call is made twice in each affected transaction, even though the answer between calls can't change.

**Recommended Mitigation:** Convert the modifier into an internal function which does the revert check and returns the rate, the pass the cached rate to any child functions that require it.

Also `ISecuritizeNavProvider::rate` returns `uint256` so the `< 0` comparison is non-sensical, just enforce that the rate is `!= 0`.

**Securitize:** Acknowledged.
