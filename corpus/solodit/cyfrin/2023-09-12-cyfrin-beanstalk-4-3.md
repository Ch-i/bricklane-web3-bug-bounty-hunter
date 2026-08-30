---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Avoid repeated comparison with `msg.sender` when looping in `SiloFacet:transferDeposits`
vuln_class: []
---

# Avoid repeated comparison with `msg.sender` when looping in `SiloFacet:transferDeposits`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Currently, `SiloFacet:transferDeposits` performs the same comparison every loop iteration, but this can be done just once outside the for loop:

```diff
// SiloFacet:transferDeposits
//...
+       bool callerIsNotSender = sender != msg.sender;
        for (uint256 i = 0; i < amounts.length; ++i) {
            require(amounts[i] > 0, "Silo: amount in array is 0");
-           if (sender != msg.sender) {
+           if (callerIsNotSender) {
                LibSiloPermit._spendDepositAllowance(sender, msg.sender, token, amounts[i]);
            }
        }
//...
```

Alternatively, the logic can be divided into two separate for loops to more efficiently handle this case:

```diff
// SiloFacet:transferDeposits
//...
+   if (sender != msg.sender){
        for (uint256 i = 0; i < amounts.length; ++i) {
            require(amounts[i] > 0, "Silo: amount in array is 0");
-           if (sender != msg.sender) {
                LibSiloPermit._spendDepositAllowance(sender, msg.sender, token, amounts[i]);
-           }
        }
+   } else {
+       for (uint256 i = 0; i < amounts.length; ++i) {
+           require(amounts[i] > 0, "Silo: amount in array is 0");
+       }
+   }
//...
```
