---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-M-4 Deposits of fee-on-transfer tokens will favor later depositors, making
  earlier investors lose funds
vuln_class: []
---

# TRST-M-4 Deposits of fee-on-transfer tokens will favor later depositors, making earlier investors lose funds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
When deposits are processed, the percentage of **Denominator** minted to the depositor is 
linear to the contribution, compared to the current balance. 
```solidity
         uint256 T = vlt.virtualTotalBalance(); //will be at least 1
         uint256 D = vlt.D();
         if (functions.willOverflowWhenMultiplied(amt, D)) {
            require(T > amt || T > D, "overflow");
         }
         deltaN = Arithmetic.overflowResistantFraction(amt, D, T);
             vlt.setN(msg.sender, vlt.N(msg.sender) + deltaN);
                  vlt.setD(D + deltaN); //D always kept = sum of all Ns, plus 
                    vlt.initD()
         for (uint256 i = 0; i < tkns.length; i++) {
            if (amts[i] > 0) {
         IERC20(tkns[i]).safeTransferFrom(msg.sender, vaultAddress, amts[i]);
            }
         }
```
The calculation will lead to incorrect results when using fee-on-transfer (tax) tokens. The 
"before-tax" amount of the depositor will be compared to the "after-tax" amount in the 
contract balance. It is exploitable by immediately withdrawing the shares, receiving more 
tokens than the amount contributed (unless fees are higher than the token tax). 

**Recommended mitigation:**
Compare the balance before and after the `safeTransferFrom()` call.

**Team response:**
"amt now calculated by comparing vault balances before and after safeTransferFrom. N and 
D updated afterwards. "
