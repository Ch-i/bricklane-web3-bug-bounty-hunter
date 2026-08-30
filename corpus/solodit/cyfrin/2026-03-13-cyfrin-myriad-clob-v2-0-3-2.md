---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Magic numbers `0` and `1` used for YES and NO outcome indices throughout the
  codebase
vuln_class: []
---

# Magic numbers `0` and `1` used for YES and NO outcome indices throughout the codebase

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** Outcome indices are hardcoded as bare integer literals `0` (YES) and `1` (NO) throughout the contracts with no named constant:

```solidity
// NegRiskAdapter.sol
manager.adminResolveMarket(evt.marketIds[i], 0); // YES wins
manager.adminResolveMarket(evt.marketIds[i], 1); // NO wins

uint256 yesTokenId = conditionalTokens.getTokenId(marketId, 0);
uint256 noTokenId  = conditionalTokens.getTokenId(marketId, 1);

// ConditionalTokens.sol
_mint(msg.sender, getTokenId(marketId, 0), amount, "");
_mint(msg.sender, getTokenId(marketId, 1), amount, "");
```

Using unnamed literals makes the intent harder to verify at a glance, increases the risk of a transposition error (passing `1` where `0` was intended), and means any future change to the outcome encoding would require hunting down every occurrence manually.

**Recommended Mitigation:** Define shared constants and use them consistently:

```solidity
uint256 internal constant YES = 0;
uint256 internal constant NO  = 1;

// Usage becomes self-documenting:
conditionalTokens.getTokenId(marketId, YES);
manager.adminResolveMarket(marketId, NO);
```

**Myriad:** Fixed in commits [`6530746`](https://github.com/Polkamarkets/polkamarkets-js/pull/126/changes/6530746f656a40e9124201ac4d0c90d0b57f8fda) and [`a7ce7a7`](https://github.com/Polkamarkets/polkamarkets-js/pull/126/changes/a7ce7a77e6639368e3fd679a87748c831ee7d45c)

**Cyfrin:** Verified.
