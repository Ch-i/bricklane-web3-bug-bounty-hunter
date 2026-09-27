---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-0-6
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[H-07] settleWithETH(...) function call will revert because of ETH refunds'
vuln_class: []
---

# [H-07] settleWithETH(...) function call will revert because of ETH refunds

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DUTCHBondingHook.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DUTCHBondingHook.sol), [`DutchAuctionMarketplace.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DutchAuctionMarketplace.sol)

**Description:**

`settleWithETH(...)` forwards all `msg.value` to `swapETHForDUTCH(...)`, which refunds unused ETH to `DutchAuctionMarketplace` after the swap. This will cause NFT purchases with ETH to revert because the `DutchAuctionMarketplace` contract doesn't implement `receive()` or `fallback()` functions.

**Impact:** `settleWithETH(...)` function DoS.

**Recommendation:** Implement a `receive()` function in the `DutchAuctionMarketplace` contract.

**Status:** Fixed

**Client response:** Fixed in [ac0dda10392af280b44d249e70230e45660fc793](https://github.com/dutch-protocol/Protocol-Contracts/commit/ac0dda10392af280b44d249e70230e45660fc793)
