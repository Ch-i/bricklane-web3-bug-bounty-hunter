---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-11
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`SecuritizeSwap::buy` should revert if `stableCoinAmount` is zero'
vuln_class: []
---

# `SecuritizeSwap::buy` should revert if `stableCoinAmount` is zero

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `SecuritizeSwap::buy` should revert if `stableCoinAmount` is zero as otherwise it means that the investor can buy `dsToken` by paying zero stable coins; this could be possible if the investor calls `buy` with a small enough `_dsTokenAmount` to trigger rounding down to zero inside `calculateStableCoinAmount`.

With `DSToken` being configured with 2 decimals this rounding down to zero won't occur in `calculateStableCoinAmount`, but if `DSToken` is ever configured with standard 18 decimals this code would become vulnerable to free minting of tokens.

**Recommended Mitigation:**
```diff
    function buy(uint256 _dsTokenAmount, uint256 _maxStableCoinAmount) public override whenNotPaused {
        require(IDSRegistryService(getDSService(REGISTRY_SERVICE)).isWallet(msg.sender), "Investor not registered");
        require(_dsTokenAmount > 0, "DSToken amount must be greater than 0");
        require(navProvider.rate() > 0, "NAV Rate must be greater than 0");

        uint256 stableCoinAmount = calculateStableCoinAmount(_dsTokenAmount);
+       require(stableCoinAmount != 0, "Paying zero not allowed");
```

**Securitize:** `SecuritizeSwap` was removed as it was deprecated.

**Cyfrin:** Verified.
