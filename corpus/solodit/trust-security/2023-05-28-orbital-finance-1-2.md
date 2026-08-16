---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-M-3 User deposits can fail despite using the correct method for calculation
  of deposit amounts
vuln_class: []
---

# TRST-M-3 User deposits can fail despite using the correct method for calculation of deposit amounts

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
Users can use the `getAmtsNeededForDeposit()` function to get the amount of tokens that 
maintain the desired proportion for vault deposits. It will perform a calculation very similar to 
the one in `ratiosMatch()`, which will verify the deposit.
```solidity
         for (uint256 i = 0; i < balances.length; i++) {
               if (i == indexOfReferenceToken) {
                amtsNeeded[i] = amtIn;
         } else {
         // amtsNeeded[i] = (amtIn * balances[i]) / 
                  balances[indexOfReferenceToken];
                     amtsNeeded[i] = Arithmetic.overflowResistantFraction(amtIn, 
                  balances[i], balances[indexOfReferenceToken]);
               }
            }
```
However, a difference between the verification function and the getter function is that the 
getter receives any reference token, while the verification will use proportions based on the 
deposit amount in the largest balance in the vault. Indeed, these fractions may differ by a 
small amount. This could cause the `getAmtsNeededForDeposit()` function to respond with 
values which will not be accepted at deposit, since they will be rounded differently.

**Recommended Mitigation:**
Calculation amounts needed using the ratio between largest balance and the deposit amount. 
This would line up the numbers as verification would expect.

**Team Response:**
"Reworked the functions.getAmtsNeededForDeposit method so that ratios are based on the 
greatest amt instead of the reference token. The "amtIn" of the reference token is rounded 
down, if needed."

**Mitigation review:**
Fix is sound.
