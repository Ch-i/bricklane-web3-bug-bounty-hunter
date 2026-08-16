---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-9
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Consider using named mapping parameters
vuln_class: []
---

# Consider using named mapping parameters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** Solidity 0.8.18 introduced named mapping parameters, allowing key and value types to be given descriptive names that appear in the source and in IDE tooling. None of the in-scope contracts use this feature, making mappings harder to read at a glance:

```solidity
// Current — intent must be inferred from context
mapping(bytes32 => Event) internal _events;
mapping(bytes32 => bool) public noPositionsRedeemed;
mapping(bytes32 => uint256) public mintedWcolPerEvent;
mapping(bytes32 => bool) public orderInvalidated;
mapping(bytes32 => uint256) public filledAmounts;
mapping(uint256 => uint256[2]) public voidedPayouts;
```

**Recommended Mitigation:** Apply named parameters consistently across the in-scope contracts:

```solidity
mapping(bytes32 eventId => Event) internal _events;
mapping(bytes32 eventId => bool) public noPositionsRedeemed;
mapping(bytes32 eventId => uint256 wcolMinted) public mintedWcolPerEvent;
mapping(bytes32 orderHash => bool) public orderInvalidated;
mapping(bytes32 orderHash => uint256 filled) public filledAmounts;
mapping(uint256 marketId => uint256[2] payouts) public voidedPayouts;
```

**Myriad:** Fixed in commit [`fc17f36`](https://github.com/Polkamarkets/polkamarkets-js/commit/fc17f36fbf8773e31fe88917ea38f6858d297e1f)

**Cyfrin:** Verified.
