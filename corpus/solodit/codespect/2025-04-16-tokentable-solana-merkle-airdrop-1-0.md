---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-merkle-airdrop-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-merkle-airdrop
title: '[L-01] Fee configuration conflict'
vuln_class: []
---

# [L-01] Fee configuration conflict

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Merkle-Airdrop.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Merkle-Airdrop.md)_

---

**Files:** [merkle-token-distributor-solana::initialize.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/merkle-token-distributor-solana/src/instructions/initialize.rs#L55), [unlocker-v2-solana::initialize.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/unlocker-v2-solana/src/instructions/initialize.rs#L67)

**Description:**

If the airdrop account in the `merkle-token-distributor-solana` program and the unlocker account in the `unlocker-v2-solana` program share the same `project_id`, they will use the same fee configuration. Since both accounts can be created permissionlessly, there is no guarantee that they are created and controlled by the same owner. This may lead to a fee configuration conflict.

**Impact:** If unlock and airdrop accounts with the same `project_id` are controlled by different owners and each wants to use a different `fee_token`, there may be some complications in fee configuration.

**Recommendation(s):** It is recommended to distinguish between the fee configuration accounts for the two accounts.

**Status:** Fixed

**Update from TokenTable:** Add distributor pubkey field as additional seeds parameter when deriving a fee account in [40ebaffac8ecbf186e0625568fb10de967340d6c](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/40ebaffac8ecbf186e0625568fb10de967340d6c).
