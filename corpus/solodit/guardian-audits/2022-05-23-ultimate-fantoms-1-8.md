---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-14 | Function Visibility Modifiers
vuln_class: []
---

# UF-14 | Function Visibility Modifiers

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

The functions `setRoyaltyAddress`, `updateSpiritRouter`, `updatePaintRouter`, `publicMint`, `setMintFees`, `enableMinting`, `disableMinting`, `setBaseURI`, `setTeamMinting`, `setMintSize`, and `sweepEthToAddress` are marked as public, but are never called from inside the contract.

**Recommendation**

These functions can be marked `external` for gas optimization.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion where appropriate.
