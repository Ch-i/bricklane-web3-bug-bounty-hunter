---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-L-3 Strategy may be initialized by attacker
vuln_class: []
---

# TRST-L-3 Strategy may be initialized by attacker

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In NyPtvFantomWftmBooSpookyV2StrategyToUsdc.sol, `initialize()` is used to bootstrap the 
strategy. However, there is no caller check, which means it is only safe if proxy is upgraded 
to the strategy and immediately calls `initialize()`, using `upgradeToAndCall()` proxy 
functionality. Otherwise, attacker may call it themself and pass malicious values for treasury 
and other important parameters.

**Recommended Mitigation:**
Consider adding initialization protection. For example, during construction set an immutable 
to be the deployer address, which is the only one that is allowed to call `initialize()`.


**Team response:**
Rejected.
