---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Emit `ETHSent` event when sending eth
vuln_class: []
---

# Emit `ETHSent` event when sending eth

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** `DepositManager::receive` emits an `ETHReceived` event when receiving eth, but `transferETHForWithdrawRequests` does not emit any events when sending eth; consider also emitting an `ETHSent` event when sending eth.

**Swell:** Fixed in commit [c82dd3c](https://github.com/SwellNetwork/v3-contracts-lst/commit/c82dd3c8ca6853816dd9f1982ab0a5ef50d78cf2).

**Cyfrin:**
Verified.
