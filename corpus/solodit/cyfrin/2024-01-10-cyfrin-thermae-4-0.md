---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-4-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: Fail fast in `_completeTransfer` by checking for incorrect address/chainId
  immediately after calling `TOKENBRIDGE.parseTransferWithPayload`
vuln_class: []
---

# Fail fast in `_completeTransfer` by checking for incorrect address/chainId immediately after calling `TOKENBRIDGE.parseTransferWithPayload`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** Fail fast in `_completeTransfer` by checking for incorrect address/chainId immediately after calling `TOKENBRIDGE.parseTransferWithPayload` per the [example code](https://docs.wormhole.com/wormhole/quick-start/tutorials/hello-token#receiving-a-token).

**Impact:** Gas optimization; want to fail fast instead of performing a number of unnecessary operations then failing later anyway.

**Proof of Concept:** Portico.sol L278-300.

**Recommended Mitigation:** Perform the L300 check immediately after L278.

**Wormhole:**
Fixed in commit 5f3926b.

**Cyfrin:** Verified.
