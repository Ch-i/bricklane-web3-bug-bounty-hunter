---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-4 It’s possible to dilute rewards per second in Gauge and Internal bribes
vuln_class: []
---

# TRST-M-4 It’s possible to dilute rewards per second in Gauge and Internal bribes

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `notifyRewardAmount()` is called to distribute new rewards to a gauge or an 
internal bribe. In particular, it increases the duration over which the rewards have to be 
distributed by **DURATION** every time it’s called:
```solidity 
    periodFinish[token] = block.timestamp + DURATION;
```
Because of this an attacker could dilute the rewards per second received by bribes and 
gauges users by calling `notifyRewardAmount()` with a new reward of 1, extending the 
duration of the rewards that are currently being distributed thus lowering the rewards per 
second received by users.

**Recommended mitigation:**
A mitigation that also have positive side-effects in lowering the attack surface is to restrict 
access to the Gauge.sol and InternalBribe.sol `notifyRewardAmount()` functions:
● Adjust `notifyRewardAmount()` in Gauge.sol to be only callable by SatinVoter.sol and
the trusted addresses responsible for sending $CASH rebases, if any.
● Adjust `notifyRewardAmount()` in InternalBribe.sol to be only callable by the 
associated gauge and Ve.sol.

**Team response:**
Fixed

**Mitigation review:**
The issue has been resolved as suggested but a new issue has been introduced, the function 
`claimFees()` in Gauge.sol will fail when calling `notifyRewardAmount()` on InternalBribe.sol 
because SatinVoter.sol does not set the **gauge** parameter in the internal bribe when a new 
gauge is created via `createGauge()`.

**Mitigation review 2:**
The introduced issue has been fixed, now `notifyRewardAmount()` in Gauge.sol is only callable 
by SatinVoter.sol and the $CASH rebase handler while `notifyRewardAmount()` in 
InternalBribe.sol is only callable by Ve.sol and the associated gauge.
