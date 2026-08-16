---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-L-2  vestedAmount and vestedAmountAtTimestamp return false information
  for instant transmutations
vuln_class: []
---

# TRST-L-2  vestedAmount and vestedAmountAtTimestamp return false information for instant transmutations

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

**Description:**
**vestedAmount()** and **vestedAmountAtTimestamp()** are view functions for user to see their
vested **amount currently and in a given timestamp respectively. The issue is that they 
assume user is on a linear vesting plan, rather than instant vesting. Therefore, they will 
display false information because instant vesting users will not receive any additional 
released amounts later.

**Recommended Mitigation:**
Add a requirement in both functions, that user is in the linear vesting plan, using the
addressToVestingCode mapping.

**Team Response:**
Issue was fixed.

**Mitigation review:**
Both functions now support linear and instant vesting. However, 
vestedAmountAtTimestamp may still return incorrect results for timestamp < time of vesting
for instant vesting. Function does not take into account timestamp of `transmute()` call.
```solidity
        if (addressToVestingCode[_vester] == 1) {
                 return addressToTotalAllocatedOutputToken[_vester];
                    } else if (addressToVestingCode[_vester] == 2) {
                        return 
                    _vestingSchedule(addressToTotalAllocatedOutputToken[_vester],
            uint64(_timestamp), _vester);
         }
```
