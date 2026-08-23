---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-M-2 Attacker can DOS deposit transactions due to strict verifications
vuln_class: []
---

# TRST-M-2 Attacker can DOS deposit transactions due to strict verifications

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
When users deposit funds to the Vault, it verifies that the proportion between the tokens 
inserted to the vault matches the current vault token balances.
```solidity
      uint256[] memory balances = vlt.balances();
          //ensure deposits are in the same ratios as the vault's current balances
          require(functions.ratiosMatch(balances, amts), "ratios don't match");
```

The essential part of the check is below:
```solidity
         for (uint256 i = 0; i < sourceRatios.length; i++) {
         // if (targetRatios[i] != (targetRatios[greatestIndex] * 
                  sourceRatios[i]) / greatest) {
               if (targetRatios[i] != 
         Arithmetic.overflowResistantFraction(targetRatios[greatestIndex], sourceRatios[i], greatest)) {
         return false;
            }
         }
```
The exact logic here is not important, but note that a small change in the balance of one of 
the vault tokens will affect the expected number of tokens that need to be inserted to 
maintain correct ratio. The exact amounts to be deposited are passed as **targetRatios**, and 
**sourceRatios** is the current balances. Therefore, an attacker can **directly transfer** a negligible 
amount of some vault token to the contract to make the amount the user specified in 
**targetRatios** not line up with the expected proportion. As a result, the deposit would revert. 
Essentially it is an abuse of the over-granular verification of ratios, leading to a DOS of any 
deposit in the mempool.

**Recommended Mitigation:**
Loosen the restriction on deposit ratios. A DOS attack should cost an amount that the vault 
creditors would be happy to live with.

**Team Response:**
"Added a new function to the VaultV2 contract, "takeBalanceSnapshot", which stores the state 
of the vault balances in a new variable. This function is called at the end of every "official" 
balance state change (Deposit, Withdraw, and Trade in the VaultManager). The ratios are 
checked against this new list instead of the actual balances."

**Mitigation review:**
The fix does not eliminate the described issue. An attacker can simply donate followed by 
deposit() of a negligible amount, in order to make takeBalancesSnapshot() get called. The new 
ratio will make the deposit getting front-ran revert.

**Team response:**
"See TRST-H-2 for solution."
