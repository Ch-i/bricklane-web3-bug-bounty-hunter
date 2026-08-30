---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-3-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: Overflow detection
vuln_class: []
---

# Overflow detection

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

The utility overflowResistantFraction() is used in various places to multiply and divide when 
the intermediate result could be above uint256.It is important to note that if the final result 
exceeds 256 bits, the function would return an incorrect number, due to overflow. In most 
cases, that scenario is impossible as the divisor is larger than the second multiplied number. 
However, in the call below in the deposit() code path, it is somewhat possible:
```solidity
          deltaN = Arithmetic.overflowResistantFraction(amt, D, T);
```
It is recommended to detect a possible overflow here. 

**Team response:**
"Added overflow detection to deltaN calculation in the deposit function."

**Mitigation review:**
Overflow check is safe. It could be argued that the T > D check is unnecessary, as that should 
never occur.
```solidity
      if (functions.willOverflowWhenMultiplied(amt, D)) {
             require(T > amt || T > D, "overflow");
      }
```
