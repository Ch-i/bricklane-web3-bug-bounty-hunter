---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-25
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-26] Create 2 Hash Collision'
vuln_class: []
---

# [L-26] Create 2 Hash Collision

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

Because of the fact that the system uses deterministic addresses, given the fact that keccak (a 32 bytes function) is truncated down to a uint160 (20 bytes), the likelihood that a clash is found is around 2^80

This makes brute-force mining a clash plausible, although extremely expensive

While the risk of mining a collision is possible, this should not be feasible for any specific Safe in the system as the cost of mining a clash is estimated in the order of billions of dollars

**Notes**

It is worth going through these notes to familiarise yourself with these types of findings

https://eips.ethereum.org/EIPS/eip-3607
https://github.com/sherlock-audit/2024-06-makerdao-endgame-judging/issues/64
https://github.com/sherlock-audit/2023-07-kyber-swap-judging/issues/90
---
