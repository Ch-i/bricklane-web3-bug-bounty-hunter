---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Missing events for `initialize` instructions in both programs
vuln_class: []
---

# Missing events for `initialize` instructions in both programs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** Neither `securitize_bridge::Initialize::handler` nor `securitize_usdc_bridge::Initialize::handler` emits an event when the bridge is first configured. All other admin state-change instructions in both programs emit events, making initialization the only unobservable admin action for off-chain indexers.

**Recommended Mitigation:** Add `BridgeInitialized` events to both programs including key configuration parameters (owner, asset_mint/usdc_mint, executor_program_id, etc.).

**Securitize:** Fixed in [ba4d07](https://github.com/securitize-io/bc-solana-bridge-sc/commit/ba4d07b6b608726502c1695c9f355791b475f766).

Added a `BridgeInitialized` event emitted from the `initialize` handler in both `securitize_bridge` and `securitize_usdc_bridge`.

**Cyfrin:** Confirmed.
