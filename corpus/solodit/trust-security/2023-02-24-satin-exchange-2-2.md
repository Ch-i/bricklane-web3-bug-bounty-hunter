---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-3 It’s possible to extend the lock of an expired veSatin
vuln_class: []
---

# TRST-L-3 It’s possible to extend the lock of an expired veSatin

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `merge()`, which is used to merge two different veSatin into one, doesn’t ensure 
that the veSatin that should be merged is not expired. This allows a user to extend a veSatin 
lock time even after it expires, something the protocol assumes not to be possible. This can 
brick emissions claims and is an extra tool an attacker can use

**Recommended Mitigation:**
In the `merge()` function require that both of the veSatin used for the merge are not expired.

**Team response:**
Fixed

**Mitigation Review:**
The issue persists because the proposed fix only checks that the veSatin with the latest 
expiry is not expired:
```solidity
    uint end = _locked0.end >= _locked1.end ? _locked0.end : 
          _locked1.end;
       require(end > block.timestamp, "expired");
``` 
An effective solution needs to ensure that both _locked0.end and _locked1.end are not 
expired:
```solidity
       uint end = _locked0.end >= _locked1.end ? _locked0.end : 
           _locked1.end;
      require(_locked0.end > block.timestamp && _locked1.end > 
  block.timestamp, "expired");
```
**Mitigation Review 2:**
The issue has been resolved as suggested
