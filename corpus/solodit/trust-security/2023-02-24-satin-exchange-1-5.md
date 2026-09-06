---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-6 _vote() doesn’t check the pool a user is voting for has a valid gauge
vuln_class: []
---

# TRST-M-6 _vote() doesn’t check the pool a user is voting for has a valid gauge

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:** 
The function `_vote()` allows veSatin holders to vote to which pool the weekly emissions 
should be redirected to but it doesn’t check the pool a user is voting for has a gauge 
associated, which could lead to emissions being lost.

**Recommended Mitigation:**
Ensure that the pool a user is trying to vote for has a valid gauge before voting on it by 
checking if isGauge[pool] it’s true:
```solidity
    if(isGauge[_gauge]) { //<== CHECK IT'S A VALID GAUGE
          int256 _poolWeight = (_weights[i] * _weight) / _totalVoteWeight;
    //
      emit Voted(msg.sender, _tokenId, _poolWeight);
    }
```

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, now the function `_vote()` skips the vote for pools 
that don’t have a valid associated gauge.
