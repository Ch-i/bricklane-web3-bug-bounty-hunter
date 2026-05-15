---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: State change without event
vuln_class: []
---

# State change without event

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** Four setter functions update addresses that gate critical protocol functionality but emit no event, making changes invisible to off-chain monitors and indexers:

- `MyriadCTFExchange::setNegRiskAdapter` - only address allowed to call `mintAllYesTokens`; controls cross-market matching
- `NegRiskAdapter::setExchange` - only address allowed to call `mintAllYesTokens` on the adapter
- `NegRiskAdapter::setTreasury` - destination for excess collateral recovered at event resolution
- `PredictionMarketV3ManagerCLOB::setNegRiskAdapter` - only address allowed to create neg-risk markets and call `adminResolveMarket` for them

```solidity
// MyriadCTFExchange.sol
function setNegRiskAdapter(address _adapter) external { negRiskAdapter = _adapter; /* no event */ }

// NegRiskAdapter.sol
function setTreasury(address newTreasury) external { treasury = newTreasury; /* no event */ }
function setExchange(address _exchange) external  { exchange = _exchange;   /* no event */ }

// PredictionMarketV3ManagerCLOB.sol
function setNegRiskAdapter(address _adapter) external { negRiskAdapter = _adapter; /* no event */ }
```

**Recommended Mitigation:** Add and emit a dedicated event in each setter, e.g.:

```solidity
event NegRiskAdapterUpdated(address indexed newAdapter);
event ExchangeUpdated(address indexed newExchange);
event TreasuryUpdated(address indexed newTreasury);
```


**Myriad:** Fixed in commit [`d6c6654`](https://github.com/Polkamarkets/polkamarkets-js/commit/d6c6654794550095a65d79be701f3e0ee7701bb3)

**Cyfrin:** Verified.
