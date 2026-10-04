---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-09-swell-hyperliquid-forwarder-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-09-Swell-HyperLiquid-Forwarder.md
tags:
- firm:codespect
- report:2025-06-09-swell-hyperliquid-forwarder
title: '[I-01] The arbitrary evmEOAToSendToAndForwardToL1 parameter allows for sending
  tokens to the wrong address'
vuln_class: []
---

# [I-01] The arbitrary evmEOAToSendToAndForwardToL1 parameter allows for sending tokens to the wrong address

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-09-Swell-HyperLiquid-Forwarder.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-09-Swell-HyperLiquid-Forwarder.md)_

---

**Files:** [`HyperliquidForwarder.sol`](https://github.com/SwellNetwork/hyperliquid-forwarder/tree/59910084b7669f721330be6dc68557b6ac747c4b/src/HyperliquidForwarder.sol#L67)

**Description:**

In the `forward(...)` function, the `msg.sender` sends his own tokens from the HyperEVM to the HyperCore where the `evmEOAToSendToAndForwardToL1` address receives them. Considering that the protocol will use 5 multi-sig addresses, such an address could be verified against them in contract level to remove the possibility of sending tokens to the wrong address.

**Status:** Fixed

**Client response:** Resolved with commit [56e4679ae55aff64738274209fb526774f3a2d54](https://github.com/SwellNetwork/hyperliquid-forwarder/commit/56e4679ae55aff64738274209fb526774f3a2d54)
