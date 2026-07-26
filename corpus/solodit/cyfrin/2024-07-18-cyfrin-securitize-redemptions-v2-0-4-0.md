---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-4-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Emission of wrong value for some events
vuln_class: []
---

# Emission of wrong value for some events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** In the `SecuritizeSwap::swap()` function, an event is emitted after a successful swap.
But the event is emitting `msg.sender` in the place of `from` value while the `msg.sender` for the function `swap()` is only issuer or master.
```solidity
SecuritizeSwap.sol
101: emit Swap(msg.sender, _valueDsToken, _valueStableCoin, _newInvestorWallet);
```
**Securitize:** We won't fix. The first argument of Buy event is `address indexed _from`, in this case the `msg.sender` is correct.

**Cyfrin:** Acknowledged.
