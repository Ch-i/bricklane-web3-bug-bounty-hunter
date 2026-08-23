---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-6 It’s never possible to vote for new pools until setMaxVotesForPool()
  is called
vuln_class: []
---

# TRST-H-6 It’s never possible to vote for new pools until setMaxVotesForPool() is called

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `_vote()` allows voting on a pool only when the current amount of votes plus the 
new votes is lower or equal to the value returned by `_calculateMaxVotePossible()`:
```solidity
        require(_poolWeights <= _calculateMaxVotePossible(_pool), "Max votes exceeded");
```
However, `_calculateMaxVotePossible()` returns 0 for every pool in which the variable 
**maxVotesForPool** has not been initialized, thus making `_vote()` revert:
```solidity
          return ((totalVotingPower * maxVotesForPool[_pool]) / 100);
```
**Recommended Mitigation:**
In `createGauge()` and `createGauge4Pool()` set **maxVotesForPool** for the pool the gauge is 
being created for to 100.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved by adding an if statement that only executes the requirement if 
**maxVotesForPool[_pool]** is bigger than zero.
