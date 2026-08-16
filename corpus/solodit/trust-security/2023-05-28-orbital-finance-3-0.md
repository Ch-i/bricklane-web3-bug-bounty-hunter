---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: Redundant ownership transfers
vuln_class: []
---

# Redundant ownership transfers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

There are several instances in the contract when ownership is transferred to the msg.sender. 
By inheriting from Ownable, this will happen automatically.
```solidity
         contract GasStation is Ownable, ReentrancyGuarded {
            mapping (address => uint256) private gasBalances;
                constructor() {
                   transferOwnership(msg.sender);
          }
```
**Team response:**
"Removed several ownership transfers."

**Mitigation review:**
Fixed.
