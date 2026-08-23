---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: In `InvestorBasedRateLimiter::_setAddressToInvestorId` first read `addressToInvestorId[investorAddress]`
  then use it in the `if` statement check
vuln_class: []
---

# In `InvestorBasedRateLimiter::_setAddressToInvestorId` first read `addressToInvestorId[investorAddress]` then use it in the `if` statement check

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** In `InvestorBasedRateLimiter::_setAddressToInvestorId` first read `addressToInvestorId[investorAddress]` then use it in the `if` statement check to save 1 storage read:
```solidity
  function _setAddressToInvestorId(
    address investorAddress,
    uint256 newInvestorId
  ) internal {
    // @audit GAS - do this first then use it in `if` check to save 1 storage read
    uint256 previousInvestorId = addressToInvestorId[investorAddress];

    // prevents creating the same existing association
    if (previousInvestorId == newInvestorId) {
      revert AddressAlreadyAssociated();
    }
```

**Ondo:**
Acknowledged.
