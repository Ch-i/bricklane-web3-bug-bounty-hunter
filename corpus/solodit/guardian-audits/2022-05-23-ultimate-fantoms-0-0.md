---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-1 | Centralization Risk
vuln_class: []
---

# UF-1 | Centralization Risk

_Section severity (from Solodit section header): Medium_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

The `owner` address, `0x3e522051a9b1958aa1e828ac24afba4a551df37d`, is not a multi-sig and has potentially dangerous permissions for `renounceOwnership`, `transferOwnership`, `setRoyaltyAddress`, `setSpiritRouter`, `updatePaintRouter`, `setBaseURI`, `setMintSize`, `sweepEthToAddress`.

**Recommendation**

Make the `owner` a multi-sig and/or introduce a timelock for improved community oversight.

**Resolution**

Ultimate Fantoms: Acknowledged, contract ownership will be changed to the multisig at
`0x87f385d152944689f92Ed523e9e5E9Bd58Ea62ef`.
