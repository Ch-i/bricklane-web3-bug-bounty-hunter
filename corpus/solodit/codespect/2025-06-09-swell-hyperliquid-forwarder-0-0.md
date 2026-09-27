---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-09-swell-hyperliquid-forwarder-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-06-09T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-09-Swell-HyperLiquid-Forwarder.md
tags:
- firm:codespect
- report:2025-06-09-swell-hyperliquid-forwarder
title: '[H-01] The HYPE bridge address is hardcoded as the WHYPE bridge address'
vuln_class: []
---

# [H-01] The HYPE bridge address is hardcoded as the WHYPE bridge address

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-09-Swell-HyperLiquid-Forwarder.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-09-Swell-HyperLiquid-Forwarder.md)_

---

**Files:** [`HyperliquidForwarder.sol`](https://github.com/SwellNetwork/hyperliquid-forwarder/tree/59910084b7669f721330be6dc68557b6ac747c4b/src/HyperliquidForwarder.sol#L45)

**Description:**

The `HyperliquidForwarder` contract has 2 hardcoded addresses:

```solidity
address public constant WHYPE = 0x5555555555555555555555555555555555555555;
address private constant WHYPE_BRIDGE = 0x2222222222222222222222222222222222222222;
```

However, according to the HyperLiquid docs ([link](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm/hypercore-less-than-greater-than-hyperevm-transfers#system-addresses)), the `0x2222222222222222222222222222222222222222` address is HYPE’s system address and not WHYPE’s. These values are implemented in the `addTokenIDToBridgeMapping(...)` function:

```solidity
function addTokenIDToBridgeMapping(address tokenAddress, address bridgeAddress, uint16 tokenID)
    public
    requiresAuth
{
    // HYPE/WHYPE is an exception and is handled separately, do not allow an owner to incorrectly set it
    if (tokenAddress == WHYPE) {
        tokenAddressToBridge[WHYPE] = WHYPE_BRIDGE;
        return;
    }
    ...
}
```

**Impact:** Any WHYPE tokens that will be sent through this contract will be lost.

**Recommendation:** Replace the WHYPE for the HYPE token to correctly use the bridge. However, HYPE transfer should be treated like native ETH transfer; therefore, the implementation of the `forward(...)` function should be changed.

**Status:** Fixed

**Client response:** Resolved with commit [56e4679ae55aff64738274209fb526774f3a2d54](https://github.com/SwellNetwork/hyperliquid-forwarder/commit/56e4679ae55aff64738274209fb526774f3a2d54)
