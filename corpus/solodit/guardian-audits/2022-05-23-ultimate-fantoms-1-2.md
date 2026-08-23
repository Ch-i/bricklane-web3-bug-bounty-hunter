---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-2
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
title: UF-8 | Unnecessary Code
vuln_class: []
---

# UF-8 | Unnecessary Code

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

Several functions such as `setMintFees`, `enableMinting`, `disableMinting`, `setTeamMinting`, `minterTeamMintsRemaining`, and `minterTeamMintsCount` serve no purpose.
In addition, variables such as `enableMinter`, `_earnAmount`, `_mintFees`, `_teamMintSize`, `RNDM_TOKEN`, `bePATH1`, `bePATH2`, `BEETS_TOKEN`, `bPath1`, `bPath2`, `BRUSH_TOKEN`, `SPIRITSWAP_TOKEN`, `wCYBERs`, `wFTMOPRs`, `OPR`, `_beetsAlloc`, `_treasuryAlloc`, `_dfyAlloc`, and `_teamMintCounter` go unused.

**Recommendation**

Remove unused code.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion
