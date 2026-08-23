---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Unused mapping
vuln_class: []
---

# Unused mapping

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

flaggedNFTS (contracts/MGD.sol#19)
The mapping is never used, though is kept on the contract and can be set through the setter.
The comment states, that the mapping is used by the frontend app, though its usage should
be verified.

**Recommendation**:

Verify the functionality.
