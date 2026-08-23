---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-5 createGauge4Pool() lacks proper checks and/or access control
vuln_class: []
---

# TRST-M-5 createGauge4Pool() lacks proper checks and/or access control

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:** 
The function createGauge4Pool() can be called by anybody at any time and is used to create 
a Gauge for a special pool, the 4pool. It takes 5 parameters as inputs: 
```solidity
    function createGauge4pool(
       address _4pool,
          address _dai,
            address _usdc,
               address _usdt,
             address _cash
       ) external returns (address) {
```
None of the parameters are properly sanitized, meaning **_dai, _usdc, _usdt, _cash** could be 
any whitelisted token and not necessarily DAI, USDC, USDT, and cash while **_4pool** could 
be any custom contract, including a malicious one.
The function also sets the variable **FOUR_POOL_GAUGE_ADDRESS** to the newly created gauge, 
overwriting the previous value.


**Recommended Mitigation:**
Make the function only callable by an admin, and if it can be called multiple times, turn the 
variable **FOUR_POOL_GAUGE_ADDRESS** to a mapping from address to boolean to support 
multiple 4 pools.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, `createGauge4Pool()` is now only callable by the 
contract owner and **FOUR_POOL_GAUGE_ADDRESS** has been turned into a mapping, 
**is4PoolGauge**.
