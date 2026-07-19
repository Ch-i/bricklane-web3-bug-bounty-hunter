---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: In `InvestorBasedRateLimiter::_setAddressToInvestorId` use `delete` when setting
  to zero for gas refund
vuln_class: []
---

# In `InvestorBasedRateLimiter::_setAddressToInvestorId` use `delete` when setting to zero for gas refund

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** In `InvestorBasedRateLimiter::_setAddressToInvestorId` use `delete` when setting to zero:
```solidity
    // If the address is not being disassociated from all investors, increment the count
    // for the investor the address is being associated with.
    if (newInvestorId != 0) {
      ++investorAddressCount[newInvestorId];

      emit AddressToInvestorIdSet(
        investorAddress,
        newInvestorId,
        investorAddressCount[newInvestorId]
      );

       // @audit move this here when setting a valid value
       addressToInvestorId[investorAddress] = newInvestorId;
    }
    else {
       // @audit use `delete` when setting to 0 for gas refund
       delete addressToInvestorId[investorAddress];
    }
```

**Ondo:**
Acknowledged.
