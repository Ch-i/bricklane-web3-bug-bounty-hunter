---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Extra variable may be omitted
vuln_class: []
---

# Extra variable may be omitted

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/MGD.sol#432, setListingFee()
contracts/MGD.sol#420, setMintFee()
contracts/MGD.sol#408, unlockPlatform()
Extra variable mgdCon may be omitted as unnecessary.

**Recommendation**:

Remove extra variable.
