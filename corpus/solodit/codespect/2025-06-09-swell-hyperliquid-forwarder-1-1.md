---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-09-swell-hyperliquid-forwarder-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-09-Swell-HyperLiquid-Forwarder.md
tags:
- firm:codespect
- report:2025-06-09-swell-hyperliquid-forwarder
title: '[I-02] There are no checks that the system address on HyperCore has sufficient
  supply'
vuln_class: []
---

# [I-02] There are no checks that the system address on HyperCore has sufficient supply

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-09-Swell-HyperLiquid-Forwarder.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-09-Swell-HyperLiquid-Forwarder.md)_

---

**Files:** [`HyperliquidForwarder.sol`](https://github.com/SwellNetwork/hyperliquid-forwarder/tree/59910084b7669f721330be6dc68557b6ac747c4b/src/HyperliquidForwarder.sol)

**Description:**

According to the [HyperLiquid documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm/hypercore-less-than-greater-than-hyperevm-transfers#caveats), when bridging tokens between HyperEVM and HyperCore, there are currently no checks to verify that the system address has sufficient supply. Furthermore, these checks cannot be implemented at the contract level, meaning transactions that send funds to the bridge cannot be reverted automatically in such cases.

Therefore, the protocol team should always exercise caution before performing large token transfers.

**Status:** Acknowledged

**Client response:** Acknowledged
