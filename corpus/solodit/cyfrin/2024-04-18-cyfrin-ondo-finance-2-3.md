---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: '`InvestorBasedRateLimiter::_initializeInvestorState` should return newly created
  `investorId` to save re-reading it from storage'
vuln_class: []
---

# `InvestorBasedRateLimiter::_initializeInvestorState` should return newly created `investorId` to save re-reading it from storage

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `InvestorBasedRateLimiter::_initializeInvestorState` should return the newly created `investorId`; this can then be used inside `checkAndUpdateMintLimit` and `checkAndUpdateRedemptionLimit` to save 1 storage read in each function. For example take `checkAndUpdateMintLimit`:
```solidity
      _initializeInvestorState(
        addresses,
        defaultMintLimit,
        defaultRedemptionLimit,
        defaultMintLimitDuration,
        defaultRedemptionLimitDuration
      );

      // @audit GAS - save 1 storage read by having _initializeInvestorState
      // return the new `investorId`
      investorId = addressToInvestorId[investorAddress];
```

This can simply become:
```solidity
investorId = _initializeInvestorState(
        addresses,
        defaultMintLimit,
        defaultRedemptionLimit,
        defaultMintLimitDuration,
        defaultRedemptionLimitDuration
      );
```

**Ondo:**
Fixed in commit [192c7ca](https://github.com/ondoprotocol/rwa-internal/commit/192c7ca26e4aeab4c322ef6c4be0f39b5be5d34d).

**Cyfrin:** Verified.
