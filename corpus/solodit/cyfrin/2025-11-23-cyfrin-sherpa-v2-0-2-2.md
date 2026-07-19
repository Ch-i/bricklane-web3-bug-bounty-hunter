---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: '`CCIPReceiver` dependency not necessary'
vuln_class: []
---

# `CCIPReceiver` dependency not necessary

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** `SherpaVault` inherits `CCIPReceiver`, but the protocol’s cross-chain flow uses CCIP burn/mint token pools rather than ad-hoc message passing. Chainlink’s [cross-chain token pattern](https://docs.chain.link/ccip/concepts/cross-chain-token/evm/tokens) on EVM chains does not require a `CCIPReceiver` implementation on the token/vault contract, only pool authorization via `mint/burn` style hooks. Keeping `CCIPReceiver` (and its `_ccipReceive` stub) increases bytecode size, deployment cost, and surface area without delivering any functionality.

Consider removing the inheritance and associated code to simplify the contract, reduce gas/bytecode footprint, and avoid implying a message-bridge dependency that isn’t actually used.

**Sherpa:** Removed in commit [`59974b2`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/59974b29c59e2cc5afce87bbfd87a625bc05a94b)

**Cyfrin:** Verified. `CCIPReceiver` dependency now removed.
