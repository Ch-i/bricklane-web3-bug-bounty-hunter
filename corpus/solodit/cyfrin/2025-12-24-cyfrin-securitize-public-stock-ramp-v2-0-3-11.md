---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Refactor `PublicStockOnRamp::initializedNavProvider`, `BaseOffRamp::nonZeroLiquidityProvider`
  into internal functions to prevent identical storage reads
vuln_class: []
---

# Refactor `PublicStockOnRamp::initializedNavProvider`, `BaseOffRamp::nonZeroLiquidityProvider` into internal functions to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `PublicStockOnRamp` has a modifier `initializedNavProvider` that reads the `navProvider` storage slot, but then later on in the functions which have this modifier (`swap, calculateDsTokenAmount`), the `navProvider` storage slot is read again even though its value has not changed.

**Impact:** Storage reads are expensive; we want to avoid reading the same storage slot multiple times when the value hasn't changed.

**Recommended Mitigation:** Refactor the modifier `initializedNavProvider` into an `internal` function:
```solidity
    function _getNavProviderStrict() internal returns(address navProviderAddr) {
        navProviderAddr = address(navProvider);
        if (navProviderAddr == address(0)) revert NavProviderNotSetError();
    }
```

Then call this internal function in `PublicStockOnRamp::swap, calculateDsTokenAmount` like this:
```solidity
ISecuritizeAmmNavProvider navProviderCache = ISecuritizeAmmNavProvider(_getNavProviderStrict());
```

Then if it didn't revert, use `navProviderCache` wherever the nav provider is required.

Do a similar optimization for `BaseOffRamp::nonZeroLiquidityProvider` used in `_redeem`.

**Securitize:** Acknowledged.
