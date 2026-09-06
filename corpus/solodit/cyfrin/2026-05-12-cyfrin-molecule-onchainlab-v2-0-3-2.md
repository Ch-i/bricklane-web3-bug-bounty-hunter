---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: 'Stuck ETH on `OnChainLabRouter` and `OnChainLab` implementation: payable surfaces
  with no recovery'
vuln_class: []
---

# Stuck ETH on `OnChainLabRouter` and `OnChainLab` implementation: payable surfaces with no recovery

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `OnChainLabRouter` exposes a `receive` payable function (line 63) and a payable `fallback` (lines 67-95). Anyone (or an integration that mistakes the Router address for an account) can send ETH to the Router. The Router has no `withdraw` function, no admin, and no role-gated recovery path, so any ETH sent directly is permanently locked. The same exposure exists on the `OnChainLab` implementation contract: it has a payable `receive` for ETH receipts, but its `withdraw` reads `token` (the ERC-6551 footer) which on the implementation contract returns garbage, so `owner` returns zero and `withdraw` is unreachable through the normal NFT-owner path. ETH sent directly to the implementation address is therefore also locked.

**Files:**

`src/core/OnChainLabRouter.sol:63, 67-95`, `src/OnChainLab.sol` (implementation contract).

**Impact:** Permanent loss of ETH sent directly to `OnChainLabRouter`. The amount is bounded by user mistakes (treating Router or impl as an account). No on-chain remediation exists short of a Beacon upgrade that adds a recovery function on the implementation.

**Recommended Mitigation:** Remove the `receive` from Router (the payable fallback is sufficient for delegatecall ETH delivery with non-empty calldata), OR add a recovery function gated by `BEACON::owner`. Same fix applies to the implementation contract: either remove direct ETH receipt or add a beacon-owner-gated recovery.

**Molecule:** Fixed in [23d7a19](https://github.com/moleculeprotocol/onchainlabs/commit/23d7a19).

**Cyfrin:** Verified.
