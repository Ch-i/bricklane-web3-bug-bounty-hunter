---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-8 protectedQuote can be manipulated by calling processDepositQueue when
  large price moves in base asset occur
vuln_class: []
---

# TRST-M-8 protectedQuote can be manipulated by calling processDepositQueue when large price moves in base asset occur

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
The protectedQuote storage variable ensures that a portion of the liquidity pool is preserved 
even in the case of a “contract adjustment event” (i.e. when the pool has become insolvent). 
However, the protectedQuote is updated on deposits and withdraws using the following 
calculation:
```solidity
       protectedQuote = (liquidity.NAV - withdrawalValue).multiplyDecimal(
       DecimalMath.UNIT - lpParams.adjustmentNetScalingFactor
      );
```
The new value depends on the Net Asset Value (NAV) of the pool which, in turn, depends on 
the current hedge and price of the base asset. If the base asset moves sharply the NAV can 
drop, which can lead to a large drop in the **protectedQuote**. 
An attacker could call **initiateDeposit** with a small amount periodically. After a week’s delay 
they are then able to call **processQueuedDeposit** with the same periodicity. They can watch 
for a sharp drop in NAV and manipulate the protectedQuote down. If the price of the base 
asset moves even further this will most likely trigger the circuit breaker for contract 
adjustments and then lock in the reduced **protectedQuote** leading to losses for LPs. 

**Recommended mitigation:**
It’s not entirely clear what a good mitigation would be. The **protectedQuote** needs to be 
updated as the pool makes profits or losses. Perhaps a calculation that limits the magnitude 
by which it can change in a single step should be considered.

**Team response:**
Not really problematic that the values are being updated. The idea behind the timing of 
updates being when deposits/withdrawals are processed is they will be blocked when circuit 
breakers are running. The free liquidity circuit breaker in particular really helps with 
preventing any potential value manipulation as flagged in this issue.
