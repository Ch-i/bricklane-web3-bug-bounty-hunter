---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-9
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`deploy-full.ts` does not verify the target Tempo network'
vuln_class: []
---

# `deploy-full.ts` does not verify the target Tempo network

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `deploy-full.ts` sends irreversible deployment and configuration transactions without checking `eth_chainId` or validating the identity of the configured TIP20Factory, TIP-403 registry, and pathUSD addresses. The script defaults to the Moderato RPC and testnet explorer. Even when an operator supplies a mainnet RPC, its final MetaMask instruction still reports testnet chain ID 42431 rather than Tempo mainnet chain ID 4217 ([Tempo network documentation](https://docs.tempo.xyz/quickstart/verify-contracts)).

**Recommended Mitigation:** Require an explicit deployment profile and expected chain ID. Before the first transaction, assert the connected chain and verify the required native predeploy identities and selector behavior. Derive the displayed chain ID and explorer from the validated profile instead of hard-coding testnet values.

**Securitize:** Fixed in [PR 17](https://github.com/securitize-io/bc-tempo-sc/pull/17).

**Cyfrin:** Verified.
