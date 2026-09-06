---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-3-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: Adding emission of events
vuln_class: []
---

# Adding emission of events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

Many of the vault functions do not emit events. It is recommended to do so for transparency 
and operation with indexers.
```solidity
         function deactivate() external nonReentrant {
              require(msg.sender == owner() || msg.sender == operator, "only own/op");
               isActive = false;
         }
         function setOperator(address operatorIn) external nonReentrant {
               require(msg.sender == owner() || msg.sender == operator, "only ownop");
         operator = operatorIn;
         }
         function setAllowOtherUsers(bool allow) external nonReentrant{
               require(msg.sender == operator, "only op");
                allowOtherUsers = allow;
         }
         function setStrategy(string calldata stratString) external nonReentrant {
            require((msg.sender == operator), "only op");
               strategy = stratString;
         }
         function setStrategyAndActivate(string calldata stratString, bool activate) external nonReentrant {
               require((msg.sender == operator), "only op");
                 strategy = stratString;
                   autotradeActive = activate;
                }
```

**Team response:**
"Added events to several VaultV2 actions. I also added a new event to VaultInfo contract to 
act as a "global" autotrade state change event, "Alert". This allows my autotrade backend to 
just check one thing to see if the autotrade state has been updated. The VaultV2 contracts 
trigger this event."

**Mitigation review:**
Events are now emitted at every important step.
