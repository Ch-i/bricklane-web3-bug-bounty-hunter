---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Forcing CCIP native fee payment results in 10 percent higher costs for `LINK`
  holders
vuln_class: []
---

# Forcing CCIP native fee payment results in 10 percent higher costs for `LINK` holders

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** CCIP allows users to pay using either `LINK` or native gas token. By hard-coding `EVM2AnyMessage::feeToken = address(0)` the protocol forces all users to pay using the native gas token.

This results in [higher costs](https://docs.chain.link/ccip/billing#network-fee-table) for `LINK` holders as CCIP offers a 10% discount for paying using `LINK`, though this does simplify the protocol implementation.

**Matrixdock:** Acknowledged.
