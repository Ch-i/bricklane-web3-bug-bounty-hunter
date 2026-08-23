---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-L-1 Attacker can take over GMXAdapter implementation contract
vuln_class: []
---

# TRST-L-1 Attacker can take over GMXAdapter implementation contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
GMXAdapter inherits from BaseExchangeAdapter. It is an implementation contract for a 
transparent proxy and has the following initializer:
```solidity
       function initialize() external initializer {
         __Ownable_init();
       }
``` 
Therefore, an attacker can call initialize() on the implementation contract and become the 
owner. At this point they can do just about anything to this contract, but it has no impact on 
the proxy as it is using separate storage. If there was a delegatecall coded in GMXAdapter, 
attacker could have used it to call an attacker’s contract and execute the SELFDESTRUCT 
opcode, killing the implementation. With no implementation, the proxy itself would not be 
functional until it is updated to a new implementation. It is ill-advised to allow anyone to have 
control over implementation contracts as future upgrades may make the attack surface 
exploitable.

**Recommended Mitigation:**
The standard approach is to call from the constructor the _disableInitializers() from Open 
Zeppelin’s Initializable module

**Team Response:**
As this has no real impact on the protocol this will not be resolved. Recommendation will be 
followed in subsequent upgrades.
