---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-5 It’s possible to DOS voting for the whole protocol
vuln_class: []
---

# TRST-H-5 It’s possible to DOS voting for the whole protocol

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `_vote()` internally calls `_calculateMaxVotePossible()`, which internally calls 
`getTotalVotingPower()` on Ve.sol, which loops over every veSatin and adds all of their 
current voting power to get the total voting power in the system. This can be an issue when 
the number of veSatin is so high that the execution would cost more gas than the maximum 
amount permitted in a block, thus making `_vote()` always revert.

**Recommended Mitigation:**
It’s possible to leverage the variable **pointHistory** in Ve.sol to get the current total amount of 
voting power in the system. An example of how this is done is in the function 
`_checkpointTotalSupply()` in VeDist.sol.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, `_calculateMaxVotePossible()` now internally 
calculates the total amount of voting power by calling `totalSupply()` on Ve.sol which uses the 
variable **pointHistory**, which does not require unbounded loops.
