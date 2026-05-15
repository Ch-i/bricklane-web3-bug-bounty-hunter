---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: Non-compliant events emitted on vault deposits and withdrawals
vuln_class: []
---

# Non-compliant events emitted on vault deposits and withdrawals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** `Vault` emits custom `Deposited` and `Withdrawn` events in `Vault::deposit`/`mint` and `withdraw`/`redeem`, while [EIP-4626](https://eips.ethereum.org/EIPS/eip-4626#events) specifies standard `Deposit` and `Withdraw` event names.

**Impact:** The implementation is non-conformant at the event level and may break tooling or integrations that rely on the canonical ERC-4626 events for indexing or accounting.

**Recommended Mitigation:** Emit standard `Deposit` and `Withdraw` events with the exact EIP-4626 signatures instead of the custom `Deposited` / `Withdrawn`.

**Lido:** Fixed in commit [`52217ad`](https://github.com/lidofinance/defi-interface/commit/52217ad4ad48f0f8fc8534e78ad1032af66c4152)

**Cyfrin:** Verified. Correct EIP-4626 events are not emitted.
