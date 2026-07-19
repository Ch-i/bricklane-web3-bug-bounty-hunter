---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-L-3 Autotrader can steal gas
vuln_class: []
---

# TRST-L-3 Autotrader can steal gas

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
The autotrader receives gas compensation for the invocation of a trade action.
```solidity
      if (useGasStation && (msg.sender == _autoTrader) && (_autoTrader != 
          vlt.operator())) { //operator pays gas to _autoTrader for auto trades
             uint256 gasPrice = tx.gasprice;
               if (gasPrice == 0){
            gasPrice = 1;
         }
         uint256 fee = gasPrice * (gasStart - gasleft() + 
      gasStationParam);
      GS.removeGas(fee, payable(_autoTrader), vlt.operator());
      }
```
Note that **tx.gasprice** is controlled by the sender, by passing an arbitrary priority fee. This way, 
the fee calculation may grant them a large profit. The key point is that **gasStationParam** is set 
in a way that the gas spent to execute the transaction would be less than the gas 
compensation.

**Team response:**
"Capped gasPrice at block.basefee*2"

**Mitigation review:**
The solution reduced the risk to an accepted level.
