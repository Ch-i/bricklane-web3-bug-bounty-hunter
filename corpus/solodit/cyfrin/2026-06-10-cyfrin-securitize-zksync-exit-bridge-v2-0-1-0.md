---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: Remove `ZKSyncSecuritizeBridge::withdrawETH` and in `bridgeDSTokens` revert
  when `msg.value > 0`
vuln_class: []
---

# Remove `ZKSyncSecuritizeBridge::withdrawETH` and in `bridgeDSTokens` revert when `msg.value > 0`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** `ZKSyncSecuritizeBridge` never uses ETH or `msg.value` but it needs the modifier `payable` on function `bridgeDSTokens` to satisfy compile-time interface requirements.

**Recommended Mitigation:** In `ZKSyncSecuritizeBridge::bridgeDSTokens` revert when `msg.value > 0` and remove function `withdrawETH`.

**Securitize:** Fixed in commit [`6ea08b4`](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/6ea08b492b95290522b016cfc5dae125ad169460)

**Cyfrin:** Verified.
