---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-7 _derivedBalance() doesn’t properly apply boosted rewards based on
  voting power
vuln_class: []
---

# TRST-L-7 _derivedBalance() doesn’t properly apply boosted rewards based on voting power

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:** 
The function `_derivedBalance()` is used to adjust the balance of a pool voter based on his 
percentage of voting power and LP deposited. However the adjustment is only applied to 
the Satin / $CASH LP gauge because the function returns earlier in any other scenario: 
```solidity
    if (underlying != IVe(ve).token()) {
        return _derived;
    }
```
This means the emissions received by a voter are not increased based on the total voting 
power they have in the system, with the exception of the Satin / $CASH LP, which is counter intuitive because users have to either lock Satin / $CASH LP in Ve.sol to get voting power or 
in the gauge to get emissions.

**Recommended mitigation:**
The team likely intended to have the opposite effect, not increasing the emissions based on 
voting power for the Satin / $CASH LP but increasing it for every other gauge:
```solidity
    if (underlying == IVe(ve).token()) { //⇐ IF EQUAL
          return _derived;
    }
```
**Team response:**
The team disputed and is aware of the issue which is considered intended behavior.
